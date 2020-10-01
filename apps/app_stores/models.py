#!/usr/bin/python3

# from django.db import models
# import datetime
# # from django_job.users.models import User

from django.db import models
from django.conf import settings


class ChargebeeData(models.Model):
    # scraping_task_desc = models.CharField(max_length=512)
    # start_time_epoch = models.IntegerField(default=0)  # when scraping was *stated*

    auth0_user_id = models.PositiveIntegerField(default=0)
    customer_id =  models.CharField(max_length=40) # Chargebee customer id


      