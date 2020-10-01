# import pytest
#
# from apps.job.forms import ScrapingTaskForm
# from apps.job.tests.factories import ScrapingTaskFactory
#
# pytestmark = pytest.mark.django_db
#
#
# class TestScrapingTaskForm:
#     def test_scraping_task(self):
#
#         proto_user = ScrapingTaskFactory.build()
#
#         form = ScrapingTaskForm(
#             {
#                 "scraping_task_desc": proto_user.scraping_task_desc,
#                 "start_time_epoch": proto_user.start_time_epoch
#             }
#         )
#
#         assert form.is_valid()
#         # Creating a task.
#         instance = form.save()
#         assert instance.scraping_task_desc == proto_user.scraping_task_desc
#         assert instance.start_time_epoch == proto_user.start_time_epoch
#
#     def test_blank_data(self):
#
#         proto_user = ScrapingTaskFactory.build()
#
#         form = ScrapingTaskForm(
#             {
#                 "scraping_task_desc": None,
#                 "start_time_epoch": None
#             }
#         )
#
#         assert (form.is_valid()==False)
#
#         assert (form.errors, {
#             'scraping_task_desc': ['required'],
#             'start_time_epoch': ['required']
#         })
#
