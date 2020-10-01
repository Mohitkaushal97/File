import os
import http.client
import json
import requests
from django.conf import settings
import logging
import environ
env = environ.Env()

from utils.singleton_class import SingletonMetaClass
# from apps.job.models import UserToken
from utils.timer_util import MyTimer
logger = logging.getLogger('database.request')

class UserTokenRM():
    def __init__(self, server_with_port):
        self._server_with_port = server_with_port

    def get_server_and_port(self):
        return self._server_with_port

    def get_token_jobs(self):
        jobs_secret_token = env.str('SECRET_AUTH__JOBS_APP_SECRETS', None)
        if jobs_secret_token is None:
            return jobs_secret_token
        bearer_access_token = "Bearer " + jobs_secret_token
        return bearer_access_token

class RequestsManager(metaclass=SingletonMetaClass):
    def __init__(self):
        self.init_request_token()
        self.session = requests.Session()
        pass

    def get__jobs_list_response(self, page=1, per_page=10):
        with MyTimer('get__jobs_list_response api', logger):
            extra_url = '/v2/jobs'
            payload = {"page": int(page), "per_page": per_page}
            url = self.user_token_rm.get_server_and_port() + extra_url
            response = self.make_request(url=url, params={}, payload=payload, method='get')
            return response

    def post__add_vote(self, request, user_id=None, job_jsha=None, vote=None, search_id=None):
        with MyTimer('add_vote api', logger):
            # tok_instance = get_token__helper_with_request(request)
            extra_url = '/v1/votes'

            payload = {"user_id": user_id, "result_sha": job_jsha, "vote": vote, "search_id": search_id}
            url = self.user_token_rm.get_server_and_port() + extra_url
            response = self.make_request(url=url, params={}, payload=payload, method='post')

            return response.json()

    def make_request(self, url, params, payload=None, method='get'):
        with MyTimer('make_request api', logger):
            headers = {
                'Content-Type': 'application/json',
            }
            token = self.user_token_rm.get_token_jobs()
            if token is not None:
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

    def get_stores_list(self, page_index, per_page, payload=None):
        return self.get_response_stores(page_index, per_page)

    def init_stores_response(self):
        per_page = 10
        for page_index in range(1, 8+1):
            file_path = os.path.join('resources', f'stores_{page_index}_{per_page}.txt')
            file_path_abs = os.path.abspath(file_path)
            assert os.path.isfile(file_path), f"Error: file [{file_path_abs}] does not exist!"  # we can assert() since this is test code!

            response = open(file_path_abs, 'r').read()
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
    def get_request_manager_jobs(self):
        if settings.MOCK_API_REQUESTS:
            logger.info(f"get_request_manager_jobs: return simulator for stores")
            return RequestsManagerSimulator()
        else:
            return RequestsManager()


