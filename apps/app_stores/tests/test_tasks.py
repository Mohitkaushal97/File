# import pytest
# from celery.result import EagerResult
# # from apps.job.tasks import get_scraping_task_count
# from apps.job.tests.factories import ScrapingTaskFactory
#
#
# @pytest.mark.django_db
# def test_scraping_task_count(settings):
#     """A basic test to execute the get_users_count Celery task."""
#     ScrapingTaskFactory.create_batch(3)
#     settings.CELERY_TASK_ALWAYS_EAGER = True
#     task_result = get_scraping_task_count.delay()
#     assert isinstance(task_result, EagerResult)
#     assert task_result.result == 3
#
#
