from django.views.generic import ListView, TemplateView
from .operations.request_manager import InjectionsManager

import logging

logger = logging.getLogger('viewes')

class JobListViewNew(TemplateView):
    template_name = 'pages/home3.html'

    def get_context_data(self, **kwargs):
        context = super(JobListViewNew, self).get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 1))
        # tok_instance = get_token__helper_with_request(self.request)

        response = InjectionsManager().get_request_manager_jobs().get__jobs_list_response(page=page, per_page=10)
        data = response.json()
        mod_data = []
        for dt in data['results']:
            temp = {}
            temp['id'] = dt['id']
            temp['job_url'] = dt['job_url']
            temp['job_title'] = dt['job_title']
            temp['found_url'] = dt['found_url']
            temp['job_location'] = dt['job_location']
            temp['full_description'] = dt['full_description']
            temp['seen_time_epoch'] = dt['seen_time_epoch']
            temp['short_description'] = dt['short_description']
            temp['tags_string'] = dt['tags_string']
            temp['job_jsha'] = dt['job_jsha']
            temp['similar_job_string'] = ""
            mod_data.append(temp)

        context['jobdescription_instances'] = mod_data
        context['pagination_data'] = data['pagination']
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

