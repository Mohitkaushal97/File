from django.test import TestCase
# import pytest
# from django.conf import settings
# from django.test import RequestFactory
#
# from apps.job.forms import ScrapingTaskForm
# from apps.job.models import ScrapingTask
# from apps.job.tests.factories import ScrapingTaskFactory
# # from apps.job.views import SingleJobTemplateView
# from django_job.users.tests.factories import UserFactory
# from django_job.users.views import UserRedirectView, UserUpdateView, User
#
# pytestmark = pytest.mark.django_db
#

import os
from pathlib import Path

from apps.job.views import JobListViewNew
# from apps.job.views_stores import StoresListView

# https://realpython.com/testing-in-django-part-1-best-practices-and-examples/
from django.test import TestCase
from django.utils import timezone
# from django.core.urlresolvers import reverse
from django.urls import resolve, reverse

class ViewsTestCase(TestCase):
    def setUp(self):
        pass
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")

    def save_response(self, resp, desc):
        path_to_save = os.path.join('output', desc+'.html')
        path_to_save_abs = os.path.abspath(path_to_save)
        path_to_save_dir = os.path.dirname(path_to_save_abs)
        Path(path_to_save_dir).mkdir(parents=True, exist_ok=True)

        print(f"saving resp with desc [{desc}] to path: [{path_to_save}] abs: [{path_to_save_abs}]")
        with open(path_to_save_abs, 'w', encoding='UTF8') as fout:
            fout.write(resp.content.decode(resp.charset))

    def test_view__stores_view(self):
        # res = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        # url = reverse("job.views.stores_view")
        url = reverse("stores_view")
        print(f"url: [{url}]")
        resp = self.client.get(url)
        print(f"resp.status_code: {resp.status_code}")

        self.save_response(resp, 'test_view__stores_view')

        # """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')

# class JobViewTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         # Create 13 authors for pagination tests
#
#
#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass
#
#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get('/job/job-description-list/')
#         self.assertEqual(response.status_code, 200)
