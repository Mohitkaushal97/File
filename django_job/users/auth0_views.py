# import json
# # from urllib import request
# # from jose import jwt
# # from social_core.backends.oauth import BaseOAuth2
#
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
# from django.contrib.auth import logout as log_out
# from django.shortcuts import render, redirect
# from django.conf import settings
# from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from urllib.parse import urlencode
#
#
# # https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/#decorating-the-class
# class auth0_sample_class_based_view(TemplateView):
#     template_name = 'auth0/dashboard.html'
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(auth0_sample_class_based_view, self).get_context_data(*args, **kwargs)
#         context['auth0User'] = 'auth0User'
#         request = self.request
#         user = request.user
#         auth0user = user.social_auth.get(provider='auth0')
#         userdata = {
#             'view_name': "dashboard_class",
#             'auth0user.uid': auth0user.uid,
#             'user.first_name': user.first_name,
#             'user.last_name': user.last_name,
#             'user.email': user.email,
#             'user.is_staff': user.is_staff,
#             'user.is_active': user.is_active,
#             'user.date_joined': str(user.date_joined),
#             'auth0user.extra_data["picture"]': auth0user.extra_data['picture'],
#             'auth0user.extra_data["email"]': auth0user.extra_data['email']
#         }
#
#         context['userdata'] = json.dumps(userdata, indent=4)
#         return context
#
#
# @login_required
# def auth0_sample_login_required_dashboard(request):
#     user = request.user
#     auth0user = user.social_auth.get(provider='auth0')
#     userdata = {
#         'auth0user.uid': auth0user.uid,
#         'user.first_name': user.first_name,
#         'user.last_name': user.last_name,
#         'user.email': user.email,
#         'user.is_staff': user.is_staff,
#         'user.is_active': user.is_active,
#         'user.date_joined': str(user.date_joined),
#         'auth0user.extra_data["picture"]': auth0user.extra_data['picture'],
#         'auth0user.extra_data["email"]': auth0user.extra_data['email']
#     }
#
#     return render(request, 'auth0/dashboard.html', {
#         'auth0User': auth0user,
#         'userdata': json.dumps(userdata, indent=4)
#     })
#
# def auth0_index_sample(request):
#     user = request.user
#     if user.is_authenticated:
#         return redirect(auth0_sample_login_required_dashboard)
#     else:
#         return render(request, 'auth0/index.html')
#
#
# def auth0_logout_sample(request):
#     log_out(request)
#     return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
#     logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
#                  (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
#     return HttpResponseRedirect(logout_url)
