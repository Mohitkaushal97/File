import os
import json
import requests
from django.conf import settings
import logging
import environ
from django.http import HttpResponseServerError

env = environ.Env()

from apps import app_stores

from utils.singleton_class import SingletonMetaClass
# from apps.job.models import UserToken
from utils.timer_util import MyTimer
logger = logging.getLogger('database.request')

class UserTokenRM():
    def __init__(self, server_with_port):
        self._server_with_port = server_with_port

    def get_server_and_port(self):
        return self._server_with_port

    def get_token_stores(self):
        stores_secret_token = env.str('AUTH__STORES_APP_SECRETS', None)
        if stores_secret_token is None:
            return stores_secret_token
        bearer_access_token = "Bearer " + stores_secret_token
        return bearer_access_token

    def get_NO_PASSWORD_configured(self):
        is_configured_NO_PASSWORD = env.bool('API__SERVER_WITH_PORT__NO_PASSWORD', False)
        return is_configured_NO_PASSWORD

class RequestsManager(metaclass=SingletonMetaClass):
    def __init__(self):
        self.init_request_token()
        self.session = requests.Session()
        pass

    # don't set payload={} as default value, since will cause a bug! see:: https://docs.python-guide.org/writing/gotchas/
    # so set payload=None
    def get_stores_list(self, page_index, per_page, payload=None):
        with MyTimer('get_stores_list api', logger):
            extra_url = f'/v2/stores/{page_index}/{per_page}'
            url = self.user_token_rm.get_server_and_port() + extra_url
            response = self.make_request(url=url, params={}, payload=payload, method='get')
            return response

    def make_request(self, url, params, payload=None, method='get'):
        with MyTimer('make_request api', logger):
            headers = {
                'Content-Type': 'application/json',
            }
            token = self.user_token_rm.get_token_stores()
            if token is None:
                if not self.user_token_rm.get_NO_PASSWORD_configured():
                    raise HttpResponseServerError()

            if token is not None:
                # API__SERVER_WITH_PORT__NO_PASS=True
                headers['Authorization'] = token

            if payload is None:
                payload = {}
            payload = json.dumps(payload)

            response = self.session.request(method.upper(), url, headers=headers, data=payload, params=params)
            return response

    def init_request_token(self):
        server_with_port = env('API__SERVER_WITH_PORT')
        self.user_token_rm = UserTokenRM(server_with_port=server_with_port)
        logger.info(f"retrieved token for server_with_port [{server_with_port}]")

class RequestsManagerSimulator(metaclass=SingletonMetaClass):
    def __init__(self):
        self.stores_key_to_response = {}
        self.init_stores_response()

        # import requests_mock

    def get_stores_list(self, page_index, per_page, payload=None):
        return self.get_response_stores(page_index, per_page)

    def build_response(self, status_code, content):
        # def res():
        r = requests.Response()
        # r.content = content
        r.json_data = json.loads(content)
        r.encoding = 'utf-8'
        r.status_code = status_code
        def json_func():
            return r.json_data
        # r.json = json.loads(content)
        r.json = json_func
        return r

    def init_stores_response(self):
        per_page = 10

        for page_index in range(1, 8+1):
            file_path = os.path.join(app_stores.__path__[0], 'operations', 'resources', f'stores_{page_index}_{per_page}.txt')
            file_path_abs = os.path.abspath(file_path)
            assert os.path.isfile(file_path), f"Error: file [{file_path_abs}] does not exist!"  # we can assert() since this is test code!

            response_content = open(file_path_abs, 'r', encoding='utf-8').read()
            response = self.build_response(200, response_content)

            self.add_response_stores(page_index, per_page, response)

    def add_response_stores(self, page_index, per_page, response):
        # from requests.models import Request
        self.stores_key_to_response[(page_index, per_page)] = response
        return self

    def get_response_stores(self, page_index, per_page):
        if (page_index, per_page) in self.stores_key_to_response.keys():
            return self.stores_key_to_response[(page_index, per_page)]

        return None


class InjectionsManager():
    def __init__(self):
        pass

    # This shall be mocked / monkeypatched :: https://stackoverflow.com/a/29256321
    def get_request_manager_stores(self):
        return RequestsManager()


