import json
# from urllib import request
# from jose import jwt
# from social_core.backends.oauth import BaseOAuth2

from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as log_out
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from urllib.parse import urlencode


# https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/#decorating-the-class
class test_app_test_view(TemplateView):
    template_name = 'pages/about3.html'

    def get_context_data(self, **kwargs):
        context = super(test_app_test_view, self).get_context_data(**kwargs)


        request = self.request
        user = request.user
        userdata = {}
        auth0user = {}
        if user.is_authenticated:
            auth0user = user.social_auth.get(provider='auth0')
            userdata = {
                'user.is_authenticated' : user.is_authenticated,
                'view_name': "test_app_test_view",
                'auth0user.uid': auth0user.uid,
                'user.first_name': user.first_name,
                'user.last_name': user.last_name,
                'user.email': user.email,
                'user.is_staff': user.is_staff,
                'user.is_active': user.is_active,
                'user.date_joined': str(user.date_joined),
                'auth0user.extra_data["picture"]': auth0user.extra_data['picture'],
                'auth0user.extra_data["email"]': auth0user.extra_data['email']
            }
        else:
            userdata = {
                'user.is_authenticated' : user.is_authenticated,
                'view_name': "test_app_test_view",
            }

        context['auth0user'] = json.dumps(auth0user, indent=4)
        context['userdata'] = json.dumps(userdata, indent=4)
        return context


def sentry_trigger_error(request):
    division_by_zero = 1 / 0

@require_POST
def test_view_only_post(request):
    data = {"result": "ok", "text": "test completed"}
    return JsonResponse(data)

@require_GET
def test_view_only_get(request):
    data = {"result": "ok", "text": "test completed"}
    return JsonResponse(data)

class test_class_only_post(View):
    # https://stackoverflow.com/a/52463240
    http_method_names = ['post']
    def post(self, request, *args, **kwargs):
        data = {"result": "ok", "text": "test completed"}
        return JsonResponse(data)

class test_class_only_get(View):
    # https://stackoverflow.com/a/52463240
    http_method_names = ['get']
    def get(self, request, *args, **kwargs):
        data = {"result": "ok", "text": "test completed"}
        return JsonResponse(data)
