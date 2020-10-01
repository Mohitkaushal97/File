# import pytest
# from django.conf import settings
# from django.urls import reverse, resolve
#
# from apps.job.forms import ScrapingTaskForm
# from apps.job.models import ScrapingTask
# from apps.job.tests.factories import ScrapingTaskFactory
#
# pytestmark = pytest.mark.django_db
#
#
# def test_detail():
#     pass
#
#     # proto_user = ScrapingTaskFactory.build()
#     # form = ScrapingTaskForm(
#     #     {
#     #         "scraping_task_desc": proto_user.scraping_task_desc,
#     #         "start_time_epoch": proto_user.start_time_epoch
#     #     }
#     # )
#     #
#     # assert form.is_valid()
#     # # Creating a task.
#     # scrapingTask = form.save()
#     # assert (
#     #     reverse("single_job_description", kwargs={"job_id": scrapingTask.id})
#     #     == f"/job/job-description/{scrapingTask.id}/"
#     # )
#     # assert resolve(f"/job/job-description/{scrapingTask.id}/").view_name == "single_job_description"
#
#
# def test_list():
#     assert reverse("api_job_descriptions") == "/job/api-jobs-description/"
#     assert resolve("/job/api-jobs-description/").view_name == "api_job_descriptions"
#
#
