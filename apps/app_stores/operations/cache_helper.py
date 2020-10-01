from django.db import models
import datetime
import logging
from django.shortcuts import render, redirect

# from apps.job.operations.get_token_and_job_response import get_jobs_with_user_and_search

logger = logging.getLogger('job')


class CacheHelper():
    pass
    # def get_key_name(self, search_id):
    #     return "searched_job_list_%s" % (search_id)

    # def helper__get_job_id_from_joblist(self, request, search_id):
    #     key = self.get_key_name(search_id)
    #     searched_job_list = request.session.get(key)
    #
    #     if searched_job_list is None or len(searched_job_list) == 0:
    #         return None
    #     job_id = searched_job_list[0]['id']
    #     return job_id

    # def helper__get_job_id_from_joblist_with_renrew(self, request, search_id):
    #     job_id = self.helper__get_job_id_from_joblist(request, search_id)
    #
    #     if job_id is None:
    #         res, status_code = get_jobs_with_user_and_search(request, user_id=request.user.id, search_id=search_id)
    #         if status_code != 200:
    #             logger.error("Can't get search result. status_code: %d" % (status_code))
    #             return redirect('search')
    #         if len(res) == 0:
    #             logger.error("No Search result found; len(res)==0")
    #             return redirect('search')
    #         self.helper__set_new_jobslist(request, search_id, res)
    #         job_id = self.helper__get_job_id_from_joblist(request, search_id)
    #
    #     return job_id

    # def helper__get_data_by_job_id(self, request, search_id, job_id):
    #     key = "searched_job_list_%s" % (search_id)
    #
    #     if request.session.get(key):
    #         searched_job_list = request.session.get(key)
    #         for curr_index, single_job in enumerate(searched_job_list):
    #             if single_job['id'] == job_id:
    #                 data = single_job
    #
    #                 searched_job_list.pop(curr_index)
    #                 request.session[key] = searched_job_list
    #
    #                 return data
    #
    #     # response = single_job_response(tok_instance, job_id)
    #     # data = response.json()
    #     #
    #     return None

    # def helper__set_new_jobslist(self, request, search_id, res):
    #     logger.info(f"setting search_id[{search_id}] with res")
    #     key = "searched_job_list_%s" % (search_id)
    #     request.session[key] = []
    #     request.session[key] = res
