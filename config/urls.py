from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
# from django.views.generic import TemplateView
from django.views import defaults as default_views

from apps.auth0login import views as auth0_views

urlpatterns = []
urlpatterns += [
    path("", include("apps.app_stores.urls")),
]

urlpatterns += [
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),

    # path('', auth0_views.auth0_index_sample),
    # path('dashboard', auth0_views.auth0_sample_login_required_dashboard, name='dashboard_main'),

    # # Your stuff: custom urls includes go here
    path('login', auth0_views.auth0_sample_login, name='login'),
    path('logout', auth0_views.auth0_sample_logout, name='logout'),

   # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
#     # path("accounts/", include("allauth.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handlers should exist in main urls.py file, not in modules file
handler404 = 'apps.app_stores.views.handler404_func'
handler500 = 'apps.app_stores.views.handler500_func'
handler400 = 'apps.app_stores.views.handler400_func'
handler403 = 'apps.app_stores.views.handler403_func'

if settings.DEBUG:
    # # This allows the error pages to be debugged during development, just visit
    # # these url in browser to see how these error pages look like.
    # urlpatterns += [
    #     path('dashboard_class_example', auth0_views.auth0_sample_class_based_view.as_view(), name='dashboard_class_example'),
    #
    #     # test
    #     path('', include('apps.test_app.urls')),
    # ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
