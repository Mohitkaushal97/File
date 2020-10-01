from django.db import models
import datetime


class JobDescription(models.Model):
    job_url = models.CharField(max_length=512)
    found_url = models.CharField(max_length=512)
    job_title = models.CharField(max_length=512)
    job_location = models.CharField(max_length=512)
    short_description = models.CharField(max_length=512)
    full_description = models.CharField(max_length=10000)
    tags_string = models.CharField(max_length=512)
    seen_time_epoch = models.IntegerField(default=0)
    # last_seen_time_epoch = models.IntegerField(default=0)

    # When job is added, it is relevant.
    # Job becomes irelevant when exists ScrapingTask of the job with start_time > last_seen_time
    # E.g., if we scraped the ScrapingTask which gave us the job in the past, but in most recent
    # run of the ScrapingTask we did not find the job.
    job_relevant = models.BooleanField(default=True)
    scraping_task_desc = models.CharField(max_length=512)

    def __eq__(self, other):
        """Override the default Equals behavior"""

        return self.job_url == other.url and \
               self.found_url == other.found_url and \
               self.job_title == other.job_title and \
               self.job_location == other.job_location and \
               self.short_description == other.short_description and \
               self.full_description == other.full_description and \
               self.tags_string == other.tags_string and \
               self.seen_time_epoch == other.seen_time_epoch and \
               self.job_relevant == other.job_relevant and \
               self.scraping_task_desc == other.scraping_task_desc


class JobSearchInfo(models.Model):
    user_id = models.PositiveIntegerField(default=0)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_search_title = models.TextField()
    initial_keywords = models.TextField(default='')
    job_search_description = models.TextField(default='')
    user_job_id = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super(JobSearchInfo, self).save(args, kwargs)


# class JobSearchResult(models.Model):
#     job_search_info = models.ForeignKey(JobSearchInfo, on_delete=models.CASCADE)
#     job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     user_id = models.PositiveIntegerField(default=0)
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user_job_id = models.PositiveIntegerField(default=0)
#
#     def save(self, *args, **kwargs):
#         super(JobSearchResult, self).save(args, kwargs)
#
