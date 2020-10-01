# from apps.job.models import ScrapingTask
# from config.celery_app import app
# import requests
# from config import celery_app
import logging
logger = logging.getLogger('testlogger')


# # @task()
# @app.task
# def fetch_url(url, **kwargs):
#     """
#     A simple task that fetches the provided URL and returns a tuple
#     with the HTTP status code and binary response body (if any)
#     """
#     logger.info('inside fetch_url; url: [%s]' % (url))
#
#     return 200, 'example of body text'
#     # r = requests.get(url, **kwargs)
#     # return (r.status_code, r.content)
#
#
# @celery_app.task()
# def get_scraping_task_count():
#     """A pointless Celery task to demonstrate usage."""
#     return ScrapingTask.objects.count()

