# from django.contrib.auth import get_user_model

# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
# from apps.job.models import ScrapingTask
#
# User = get_user_model()
#
#
# class ScrapingTaskForm(forms.ModelForm):
#     class Meta:
#         model = ScrapingTask
#         fields = ('id', 'scraping_task_desc', 'start_time_epoch')
from django import forms

class StudentForm(forms.Form):  
    firstname = forms.CharField(label="Enter first name",max_length=50)  
    lastname  = forms.CharField(label="Enter last name", max_length = 100)  

  