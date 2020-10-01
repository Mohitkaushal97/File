#!/usr/bin/python3
import json
import logging

import chargebee
from chargebee import InvalidRequestError

from utils.sentry_wrapper import SentryInit
from utils.singleton_class import SingletonMetaClass
from utils.timer_util import MyTimer

logger = logging.getLogger("payments")

class ChargebeeManager(metaclass=SingletonMetaClass):
    def __init__(self):
        self.is_configured = False

        if not self.is_configured:
            try:
                from django.conf import settings

                settings__CRB_SITE = settings.CRB_SITE
                settings__CRB_API_KEY = settings.CRB_API_KEY
                if settings__CRB_SITE is not None and settings__CRB_API_KEY is not None:
                    self.init(settings__CRB_SITE, settings__CRB_API_KEY)
            except Exception as ex:
                print(f"failed to auto-init ChargebeeManager: ex[{str(ex)}]")

    def init(self, crb_site, crb_api_key):
        self.crb_site = crb_site
        self.crb_api_key = crb_api_key

        chargebee.configure(api_key=self.crb_api_key, site=self.crb_site)
        self.is_configured = True

        return self

    def get_site(self):
        return self.crb_site

    # # https://apidocs.chargebee.com/docs/api/customers#retrieve_a_customer
    # def create_customer_v2(self, email, first_name=None, last_name=None, locale=None):
    #     data = {}
    #     if email is not None and len(email) > 0:
    #         data['email'] = email
    #
    #     if first_name is not None and len(first_name) > 0:
    #         data['first_name'] = first_name
    #     if last_name is not None and len(last_name) > 0:
    #         data['last_name'] = last_name
    #     if locale is not None and len(locale) > 0:
    #         data['locale'] = locale
    #
    #     try:
    #         result = chargebee.Customer.create(data)
    #         return result.customer
    #     except InvalidRequestError as e:
    #         return None

    # https://apidocs.chargebee.com/docs/api/customers#retrieve_a_customer
    def create_customer_v3(self, email, first_name=None, last_name=None, auth0_uid=None):
        data = {}
        if email is not None and len(email) > 0:
            data['email'] = email

        if first_name is not None and len(first_name) > 0:
            data['first_name'] = first_name
        if last_name is not None and len(last_name) > 0:
            data['last_name'] = last_name

        # https://apidocs.chargebee.com/docs/api/v1/customers#customer_meta_data
        if auth0_uid is not None:
            data['meta_data'] = json.dumps({'auth0_uid': auth0_uid})

        try:
            with MyTimer(f"creating crb user for email {email}", logger=logger) as _:
                result = chargebee.Customer.create(data)
            return result.customer
        except InvalidRequestError as e:
            return None


    def checkout_new_or_existing(self, crb_user_id, plan_id):
        # https://apidocs.chargebee.com/docs/api/hosted_pages#checkout_new_subscription

        checkout_new = False
        subscription_data = {'plan_id': plan_id}
        subscription_id = self.get_subscription_for_user(crb_user_id)
        logger.info(f"for crb_user_id [{crb_user_id}] got subscription_id [{subscription_id}]")
        if subscription_id is not None:
            subscription_data['id'] = subscription_id
        else:
            checkout_new = True
        checkout_data = ({
            'subscription': subscription_data,
            'customer': {'id': crb_user_id},
        })

        try:
            if checkout_new:
                with MyTimer(f"hostedpage checkout_new for crb_user_id [{crb_user_id}]", logger=logger) as _:
                    result = chargebee.HostedPage.checkout_new(checkout_data)
            else:
                with MyTimer(f"hostedpage checkout_existing for crb_user_id [{crb_user_id}]", logger=logger) as _:
                    result = chargebee.HostedPage.checkout_existing(checkout_data)

            return result
            # if checkout.hosted_page.state == 'created':
            #     return checkout.hosted_page
        except InvalidRequestError as ex:
            print(ex)
            raise ex

    def get_subscription_for_user(self, crb_user_id):
        try:
            customer_data = {'customer_id[is]': crb_user_id}

            # https://github.com/chargebee/chargebee-python/blob/master/chargebee/models/subscription.py#L29
            # customer_id
            with MyTimer(f"getting subscriptions list for crb_user_id {crb_user_id}", logger=logger) as _:
                result = chargebee.Subscription.list(customer_data)
            if len(result) >= 2:
                SentryInit().capture_exception(Exception(f"for user crb_user_id {crb_user_id} total of [{len(result)}] >= 2 subscriptions"))
                logging.error(f"for user crb_user_id {crb_user_id} total of [{len(result)}] >= 2 subscriptions")

            if len(result) > 0:
                first_id = result[0].subscription.id
                return first_id

            return None
        except InvalidRequestError as ex:
            print(ex)
            SentryInit().capture_exception(ex)
            # logger.error(ex)
            raise ex


    def get_hosted_page_id(self, hosted_page_id):
        # https://django.cowhite.com/blog/integrating-chargebee-with-django/
        # The page id is passed in as url parameter 'id'
        with MyTimer(f"retrieve-ing hosted page for hosted_page_id [{hosted_page_id}]", logger=logger) as _:
            plan = chargebee.HostedPage.retrieve(hosted_page_id)
        page = plan.hosted_page
        # if page is None:
        # # The page id is invalid handle it appropriately
        #
        if page is None:
            return None
        else:
            return page
        # elif page.state == 'succeeded':
        #     return True
        # Payment is done. Hadle appropriately

        # else  # page.state == 'cancelled':
    # Payment has been cancelled. Handle appropriately


def test_02_retrieve_or_create_customer():
    email = "test_yyy@gmail.com"
    first_name = "john"
    last_name = "doe 4"
    auth0_user_id = 12345
    customer = ChargebeeManager().create_customer_v3(email, first_name, last_name, auth0_uid=auth0_user_id)
    print("customer:", customer)
    customer_id = customer.id
    customer_meta_data = customer.meta_data
    auth0_user_id_actual = customer_meta_data['auth0_user_id']


def do_tests():
    # do_test_01_create_customer()
    test_02_retrieve_or_create_customer()

if __name__ == '__main__':
    do_tests()
