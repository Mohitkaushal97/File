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
from .views import JobListViewNew
# from .views_stores import StoresListView
# from .views import auth0_sample_login_required_dashboard, auth0_index_sample
# from .views import JobSearch_NoSid, JobSearch_NoSid_YesJid
# from .views import JobSearch_YesSid, JobSearch_YesSid_YesJid, JobRedirectView

urlpatterns = [
    path('jobs', JobListViewNew.as_view(), name='home'),


    # path('stores/<int:page_id>', StoresListView.as_view(), name='stores_view'),
    # path('', StoresListView.as_view(), name='stores_view'),
    # path('stores', StoresListView.as_view(), name='stores_view'),
    # path('search_sample', StoresListView.as_view(), name='search'),

    # path('job-description-list/', JobListView.as_view(), name='job_descriptions_list'),

    # path('', auth0_index_sample),
    # path('dashboard', auth0_sample_login_required_dashboard, name='job_descriptions_list'),

    # # list of all job searches
    # path('search', AddJobSearchTemplateView.as_view(template_name='pages/search.html'), name='search'),

    # # new - search with id 0 as default
    # path('search-new/', JobSearch_NoSid.as_view(template_name='pages/single_job_new.html'), name='job_search_new'),
    # path('search-new/<int:job_id>', JobSearch_NoSid_YesJid.as_view(), name='job_search_with_jobid_new'),

    # # new - search with id not default ; id is being retrieved from the URL
    # path('search-new-with-sid/<int:search_id>', JobSearch_YesSid.as_view(template_name='pages/single_job_with_sid_new.html'), name='job_search_with_sid_new'),
    # path('search-new-with-sid/<int:search_id>/<int:job_id>', JobSearch_YesSid_YesJid.as_view(), name='job_search_with_sid_and_jid_new'),


    # # which one of these URLs do we need?
    # path('search/top/<int:search_id>', TopJobListView.as_view(), name='top_search_jobs'),
    # path('search/do/<int:user_job_id>', SearchJobView.as_view(template_name='pages/search_job.html'), name='do_search'),
    # path('job-search-info-list', JobSearchInfoList.as_view(template_name='pages/searches_list.html'), name='job_search_info_list'),

    # path('job_redirect/<int:job_id>', JobRedirectView.as_view(), name='job_redirect'),
]

