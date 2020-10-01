#!/usr/bin/python3
import logging
import base64
import pandas as pd
import csv
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.views.generic import View, ListView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# from django.shortcuts import render_to_response # deprecated
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.http import require_http_methods, require_POST, require_GET
import sentry_sdk
from .forms import StudentForm
import chargebee
from apps.auth0login.logic.chargebee.crb_utils import ChargebeeManager
from apps.auth0login.logic.auth0_logic.auth_logic import Auth0Manager
from .operations.request_manager import InjectionsManager
from apps.auth0login.logic.session_tools import SessionTools
from apps.auth0login.logic.auth_payments_connector import AuthPaymentsManager
# from .operations.request_manager import RequestsManager, RequestsManagerSimulator

logger = logging.getLogger('viewes')
mod_data = []
# https://stackoverflow.com/a/24725091
#  defaults.server_error(request, template_name='500.html')¶
def handler404_func(request, exception, template_name="templates_stores/stores_404.html"):
    sentry_sdk.capture_exception(exception)

    response = render(request, template_name)
    response.status_code = 404
    return response

#  defaults.server_error(request, template_name='500.html')¶
def handler500_func(request, template_name="templates_stores/stores_500.html"):
    response = render(request, template_name)
    response.status_code = 500
    return response

# bad request
def handler400_func(request, exception, template_name="templates_stores/stores_500.html"):
    sentry_sdk.capture_exception(exception)

    response = render(request, template_name)
    response.status_code = 400
    return response

# forbidden
# https://docs.djangoproject.com/en/3.1/ref/views/#the-403-http-forbidden-view
def handler403_func(request, exception, template_name="templates_stores/stores_500.html"):
    sentry_sdk.capture_exception(exception)

    response = render(request, template_name)
    response.status_code = 403
    return response


class StoresListView(TemplateView):
    template_name = 'templates_stores/stores.html'

    def get_context_data(self, request, **kwargs):
        
        context = super(StoresListView, self).get_context_data(**kwargs)

        
        s_date = request.GET.get('per_page', 10)
        page_index = int(self.request.GET.get('page', 1))
        response = InjectionsManager().get_request_manager_stores().get_stores_list(page_index=page_index, per_page=s_date)
        data = response.json()
        
        for dt in data['results']:
            temp = {}
            temp['id'] = dt['id']

            temp['store_url'] = dt['store_url']
            temp['store_name'] = dt['store_name']
            temp['store_description'] = dt['store_description']
            temp['instagram_url'] = dt['instagram_url']
            temp['fb_url'] = dt['fb_url']

            temp['total_products'] = dt['total_products']
            temp['avg_prod_price'] = dt['avg_prod_price']

            temp['fb_url'] = dt['fb_url']
            temp['twitter_url'] = dt['twitter_url']
            temp['linkedin_url'] = dt['linkedin_url']
            temp['instagram_url'] = dt['instagram_url']
            temp['youtube_url'] = dt['youtube_url']
            temp['pinterest_url'] = dt['pinterest_url']

            mod_data.append(temp)

        
        context['stores_instances'] = mod_data
        print(mod_data)
        context['pagination_data'] = data['pagination']
        return context






        






           

    def get(self, request, *args, **kwargs):


        context = self.get_context_data(request,**kwargs)
        return self.render_to_response(context)





class DownloadStoreList(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        print(mod_data)

        df = pd.DataFrame(mod_data)
        response['Content-Disposition'] = 'attachment; filename="file.csv"'
        df.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
        return response

        



class StoresViewPricingV2(TemplateView):
    template_name = 'templates_stores/stores_pricing_v2.html'

    def enrich_user_info(self):
        request = self.request
        user = request.user
        auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = None, None, None, None
        if user.is_authenticated:
            auth0user = user.social_auth.get(provider='auth0')
            auth0_uid = auth0user.uid
            auth0_first_name = auth0user.user.first_name
            auth0_last_name = auth0user.user.last_name
            auth0user_email = auth0user.user.email

        return auth0_uid, auth0_first_name, auth0_last_name, auth0user_email

    def get_context_data(self, **kwargs):
        context = super(StoresViewPricingV2, self).get_context_data(**kwargs)

        auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = self.enrich_user_info()
        context['auth0_uid'] = auth0_uid
        context['auth0user_email'] = auth0user_email

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class StoresViewReturnPageV2(TemplateView):
    template_name = 'templates_stores/stores_pre_purchase.html'

    def get_context_data(self, **kwargs):
        context = super(StoresViewReturnPageV2, self).get_context_data(**kwargs)

        hosted_page_id = self.request.GET.get('hpid', None)
        # page = ChargebeeManager().get_subscription_for_user(crb_user_id="169yHES8UD5A96j1")

        page = ChargebeeManager().get_hosted_page_id(hosted_page_id=hosted_page_id)
        customer_id = page.content.customer.id
        subscription_id = page.content.subscription.id
        plan_id = page.content.subscription.plan_id

        # customer_id = self.request.GET.get('cid', None)
        # plan_id = self.request.GET.get('pid', None)
        logger.info(f"got customer_id [{customer_id}] plan_id [{plan_id}] subscription_id [{subscription_id}]")
        context['customer_id'] = customer_id
        context['subscription_id'] = subscription_id
        context['plan_id'] = plan_id
        #
        # auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = extract_user_info(self.request)
        # context['auth0_uid'] = auth0_uid
        # context['auth0user_email'] = auth0user_email

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        subscription_id = context['subscription_id']
        customer_id = context['customer_id']
        plan_id = context['plan_id']
        # auth0_uid = context['auth0_uid']
        # auth0user_email = context['auth0user_email']
        #
        # logger.info(f"getting crb_user_id for auth0_uid [{auth0_uid}]")
        # crb_userid, crb_site = get_or_create_crb_user(auth0_uid, auth0user_email, create_if_dont_exist=False)
        #
        # # verification:
        # # need to verify customer_id is what we have in auth0 data
        # # why? because otherwise users could pretend to be other users (given customer_id)..
        #
        # logger.info(f"from request got_customer_id: [{got_customer_id}] from crb: [{crb_userid}]")
        # if got_customer_id != crb_userid:
        #     logger.error(f"not equal customer id!!! request got_customer_id: [{got_customer_id}] from crb: [{crb_userid}]")
        #     return HttpResponseBadRequest(content='bad request parameters')
        #
        #
        # subscription, customer = ChargebeeManager().get_subscription(subscription_id=got_subscription_id)
        # if subscription is None or customer is None:
        #     logger.error(f"subscription or customer are None!")
        #     return HttpResponseBadRequest(content='bad request parameters')
        #
        # # verify the specified subscription belongs to the given user
        # if customer.id != crb_userid:
        #     logger.error(f"error with customer id: customer.id [{customer.id}] crb_userid [{crb_userid}]")
        #     return HttpResponseBadRequest(content='bad request parameters')
        #
        #
        # # # context['crb_userid'] = crb_userid
        # # hosted_page = ChargebeeManager().create_checkout(crb_user_id=crb_userid, plan_id='cbdemo_free')
        # # logger.info(f"retrieved hosted_page [{str(hosted_page.url)}]")
        # # redirect is shotcut for HttpResponseRedirect: https://realpython.com/django-redirects/#django-redirects-a-super-simple-example
        # return redirect(reverse('view_stores_home'))

class StoresViewPrePurchaseDebug(TemplateView):
    template_name = 'templates_stores/stores_pre_purchase.html'

    def get_context_data(self, **kwargs):
        context = super(StoresViewPrePurchaseDebug, self).get_context_data(**kwargs)

        auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = extract_user_info(self.request)

        context['auth0_uid'] = auth0_uid
        context['auth0user_email'] = auth0user_email

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        auth0user_email = context['auth0user_email']
        auth0_uid = context['auth0_uid']

        crb_userid, crb_site = get_or_create_crb_user(auth0_uid, auth0user_email)

        context['crb_userid'] = crb_userid

        # hosted_page = ChargebeeManager().create_checkout(crb_user_id=crb_userid, plan_id='cbdemo_free')
        # logger.info(f"retrieved hosted_page [{str(hosted_page.url)}]")
        # context['hosted_page_url'] = hosted_page.url
        # return self.render_to_response(context)

class StoresViewPortal(TemplateView):
    template_name = 'templates_stores/stores_portal.html'

    def get_context_data(self, **kwargs):
        context = super(StoresViewPortal, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

# @csrf_exempt    ## TODO: This is for test only! Add CSRF Support..
@require_POST
def generate_checkout_url(request):
    plan_id = None
    if 'plan_id' in request.POST:
        plan_id = request.POST['plan_id']
    if plan_id is None:
        return HttpResponseBadRequest("no plan_id specified")

    auth0_uid, auth0_first_name, auth0_last_name, auth0user_email = SessionTools.extract_user_info(request)
    crb_userid, crb_site = AuthPaymentsManager.get_or_create_crb_user(auth0_uid, auth0user_email)

    # get_subscription_for_user
    # subscription_id = ChargebeeManager().get_subscription_for_user(crb_user_id=crb_userid)
    result = ChargebeeManager().checkout_new_or_existing(crb_user_id=crb_userid, plan_id=plan_id)


    # result = chargebee.HostedPage.checkout_new({
    #     "subscription": {
    #         # "plan_id": "cbdemo_dave-sub1"
    #         "plan_id": plan_id
    #         # "plan_id": "cbdemo_scale"
    #     },
    # "customer" : {
    #   "first_name" : "fnamepython",
    #   "last_name" : "lnamepython",
    #   # "company" : request.form.get("company"),
    #   # "phone" : request.form.get("phone"),
    #   "email" : "emailpython_hhmm@gmail.com"
    # }
    # })
    # hosted_page = result._response['hosted_page']

    hosted_page = result._response['hosted_page']
    data = hosted_page
    resp = JsonResponse(data)
    return resp


# https://www.chargebee.com/checkout-portal-docs/api-portal.html#integration-steps
# @csrf_exempt    ## TODO: This is for test only! Add CSRF Support..
@require_POST
def create_portal_session(request):
    # chargebee.configure("test_jqXGuQLkBHUSR2PM0qgUV21W1VqSFJIU", "honeycomics-v3-test")
    chargebee.configure("test_qDNCoDWdlzgkepytSgFgcucch5lrqWXsh", "cartstuff-test")

    result = chargebee.PortalSession.create({
        "customer": {
            "id": "AzqgjFS8UDtnD7cf"        # lilachik1985+leopard.t7@gmail.com
        }
    })
    portal_session = result._response['portal_session']
    data = portal_session
    return JsonResponse(data)

