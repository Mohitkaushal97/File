#!/usr/bin/python3
import os
import json
import requests
import urllib.parse
import environ
import logging


from utils.singleton_class import SingletonMetaClass
from utils.timer_util import MyTimer

env = environ.Env()
DOT_ENV_PATH = env.str("DOT_ENV_PATH", default=None)
if DOT_ENV_PATH:
    env.read_env(DOT_ENV_PATH)

logger = logging.getLogger("payments")

class Auth0Manager(metaclass=SingletonMetaClass):
    def __init__(self):
        self.is_configured = False

        self.token_type = None
        self.access_token = None

        if not self.is_configured:
            try:
                from django.conf import settings

                settings__SOCIAL_AUTH_AUTH0_DOMAIN = settings.SOCIAL_AUTH_AUTH0_DOMAIN
                settings__SOCIAL_AUTH_AUTH0_KEY = settings.SOCIAL_AUTH_AUTH0_KEY
                settings__SOCIAL_AUTH_AUTH0_SECRET = settings.SOCIAL_AUTH_AUTH0_SECRET
                if settings__SOCIAL_AUTH_AUTH0_DOMAIN is not None and settings__SOCIAL_AUTH_AUTH0_KEY is not None and settings__SOCIAL_AUTH_AUTH0_SECRET is not None:
                    self.init(settings__SOCIAL_AUTH_AUTH0_DOMAIN, settings__SOCIAL_AUTH_AUTH0_KEY, settings__SOCIAL_AUTH_AUTH0_SECRET)
            except Exception as ex:
                print(f"failed to auto-init Auth0Manager: ex[{str(ex)}]")


    def init(self, settings__SOCIAL_AUTH_AUTH0_DOMAIN, settings__SOCIAL_AUTH_AUTH0_KEY, settings__SOCIAL_AUTH_AUTH0_SECRET):
        self.settings__SOCIAL_AUTH_AUTH0_DOMAIN = settings__SOCIAL_AUTH_AUTH0_DOMAIN
        self.settings__SOCIAL_AUTH_AUTH0_KEY = settings__SOCIAL_AUTH_AUTH0_KEY
        self.settings__SOCIAL_AUTH_AUTH0_SECRET = settings__SOCIAL_AUTH_AUTH0_SECRET

        self.get_api_key()

        # chargebee.configure("test_qDNCoDWdlzgkepytSgFgcucch5lrqWXsh", "cartstuff-test")
        self.is_configured = True

        return self

    def get_api_key(self):
        # https://manage.auth0.com/dashboard/us/dev-env-jobs/apis/5ee9da364e38c500267a02d6/test
        # url = 'https://dev-env-jobs.us.auth0.com/oauth/token'
        headers = {'content-type': 'application/json'}
        payload = {"client_id": self.settings__SOCIAL_AUTH_AUTH0_KEY,
                   "client_secret": self.settings__SOCIAL_AUTH_AUTH0_SECRET,
                   "audience": "https://dev-env-jobs.us.auth0.com/api/v2/",
                   "grant_type": "client_credentials"
                   }

        url = rf'https://{self.settings__SOCIAL_AUTH_AUTH0_DOMAIN}/oauth/token'
        with MyTimer(f"auth0 getting api key for domain [{self.settings__SOCIAL_AUTH_AUTH0_DOMAIN}]", logger=logger) as _:
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        # logger.info("response:", response)
        response_json = response.json()
        token_type, access_token = response_json['token_type'], response_json['access_token']

        self.token_type = token_type
        self.access_token = access_token
        return token_type, access_token

    # def get_user_by_email(self, email):
    #     url_base = rf'https://{self.settings__SOCIAL_AUTH_AUTH0_DOMAIN}/api/v2/users'
    #
    #     headers = {'authorization': f'{self.token_type} {self.access_token}'}
    #
    #     # u = "/YOUR_DOMAIN/api/v2/users?q=email%3A%22jane%40exampleco.com%22&search_engine=v3"
    #
    #     # email = "jane@exampleco.com"
    #     email_encoded = urllib.parse.quote(email)
    #     url = f"{url_base}?q=email={email_encoded}&search_engine=v3"
    #
    #     with MyTimer(f"auth0 user by email for email [{email}]", logger=logger) as _:
    #         resp = requests.request("GET", url, headers=headers)
    #     print("resp:", resp)
    #     resp_json = resp.json()

    def update_metadata(self, auth0_user_id, crb_userid, crb_site=None):
        # https://auth0.com/docs/users/update-metadata-with-the-management-api

        url_base = rf'https://{self.settings__SOCIAL_AUTH_AUTH0_DOMAIN}/api/v2/users/'
        url = url_base + auth0_user_id

        headers = {'authorization': f'{self.token_type} {self.access_token}', 'content-type': 'application/json'}

        # https://stackoverflow.com/a/26685359
        # could either send "json=payload" OR data=json.dumps(payload)
        # If we send data=... so have to specify application/json content type
        payload = {'app_metadata': {'crb_userid': crb_userid}}
        if crb_site is not None:
            payload['app_metadata']['crb_site'] = crb_site

        with MyTimer(f"auth0 updating metadata auth user_id [{auth0_user_id}]", logger=logger) as _:
            resp = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))

        print("resp:", resp)
        resp_json = resp.json()

    def get_metadata(self, auth0_user_id):
        # https://auth0.com/docs/users/metadata
        # https://auth0.com/docs/users/metadata
        url_base = rf'https://{self.settings__SOCIAL_AUTH_AUTH0_DOMAIN}/api/v2/users/'

        headers = {'authorization': f'{self.token_type} {self.access_token}'}

        url = url_base + auth0_user_id
        with MyTimer(f"auth0 getting metadata auth user_id [{auth0_user_id}]", logger=logger) as _:
            resp = requests.request("GET", url, headers=headers)
        print("resp:", resp)
        resp_json = resp.json()
        app_metadata = None
        if 'app_metadata' in resp_json.keys():
            app_metadata = resp_json['app_metadata']

        return app_metadata

    def get_metadata_crb_userid(self, auth0_user_id):
        crb_userid, crb_site = None, None

        app_metadata = self.get_metadata(auth0_user_id)
        if app_metadata is not None and 'crb_userid' in app_metadata:
            crb_userid = app_metadata['crb_userid']
        if app_metadata is not None and 'crb_site' in app_metadata:
            crb_site = app_metadata['crb_site']

        return crb_userid, crb_site

def do_tests():
    pass

if __name__ == '__main__':
    do_tests()
