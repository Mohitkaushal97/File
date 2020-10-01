"""jobs_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
# from .views import StoresListView, StoresViewPricing, handler404_func
from .views import StoresListView, handler404_func
from . import views
from .views import DownloadStoreList

urlpatterns = [
    path('', StoresListView.as_view(), name='view_stores_home'),
    path('stores', StoresListView.as_view(), name='view_stores_stores'),
    path('search', StoresListView.as_view(), name='view_stores_search'),
    # path('pricing', StoresViewPricing.as_view(), name='view_stores_pricing'),
    path('pricing', views.StoresViewPricingV2.as_view(), name='view_stores_pricing'),
    # path('pricing_v2', views.StoresViewPricingV2.as_view(), name='view_stores_pricingv2'),
    path('portal', views.StoresViewPortal.as_view(), name='view_stores_portal'),
    # path('pre_purchase', views.StoresViewPrePurchase.as_view(), name='view_stores_pre_purchase'),
    # path('return_page', views.StoresViewReturnPage.as_view(), name='view_stores_return_page'),
    # path('return_page_v2', views.StoresViewReturnPageV2.as_view(), name='view_stores_return_page_v2'),
    path('return_page', views.StoresViewReturnPageV2.as_view(), name='view_stores_return_page_v2'),

    # debug
    path('pre_purchase__debug', views.StoresViewPrePurchaseDebug.as_view(), name='view_stores_pre_purchase_debug'),

    # webhooks
    # path('cb_api/generate_checkout_existing_url', views.generate_checkout_existing_url, name='generate_checkout_existing_url'),
    path('crb_api/generate_checkout_url', views.generate_checkout_url, name='generate_checkout_url'),
    path('crb_api/create_portal_session', views.create_portal_session, name='create_portal_session'),

    # path('webhook/webhook_test_1', views.Webhook_webhook_test_1, name='webhook_test_1'),

    path('', StoresListView.as_view(), name='home'),  # TODO: remove and remove from templates as well
    path('', StoresListView.as_view(), name='search'),  # TODO: remove and remove from templates as well
    path('download', DownloadStoreList.as_view(), name='views_download_stores'),
    

]


