from django.urls import path, include

from . import views

urlpatterns = [
    path('test_view', views.test_app_test_view.as_view()),
    path('sentry_error_test', views.sentry_trigger_error),

    path('test_view_only_post', views.test_view_only_post),
    path('test_view_only_get', views.test_view_only_get),
    path('test_class_only_post', views.test_class_only_post.as_view()),
    path('test_class_only_get', views.test_class_only_get.as_view()),
]
