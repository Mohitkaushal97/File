# import os
# from django.core.management.base import BaseCommand
# import logging
# from apps.job.models import UserToken
#
# # from apps.job.operations.importer import ImporterClass
#
#
# PROJECT_PATH = os.path.abspath("../../../django_job/static")
#
# logger = logging.getLogger(__name__)
#
# import environ
# env = environ.Env()
#
#
# class Command(BaseCommand):
#     def add_arguments(self, parser):
#         # parser.add_argument('file_path', nargs='+', type=str)
#         pass
#
#     def handle(self, *args, **options):
#         # server_with_port = 'http://jobs-api-dev-21.herokuapp.com:80'
#         server_with_port = env('API__SERVER_WITH_PORT')
#
#         token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UTkRRekl4TXpJNU1qRXdOalpETXpGRlJEazFSamhGTTBGQ01qSTFSamhHTUVVeE1qZENOQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNmhnaHFwMy5hdXRoMC5jb20vIiwic3ViIjoiNU5wYzZEckF3TFhoWHh6OU4zOUpWVGUwWTE2OGxYdnFAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vZGV2LWw2aGdocXAzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNTc5NjEyNzQyLCJleHAiOjE1Nzk2OTkxNDIsImF6cCI6IjVOcGM2RHJBd0xYaFh4ejlOMzlKVlRlMFkxNjhsWHZxIiwic2NvcGUiOiJjcmVhdGU6bG9nX3N0cmVhbXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.cNE_Q1STnwySBVtuhSAFMAD6wzkRQwdbeWZ8IwGBE2Bb_5Y04_3p5XtbHBFlC_Yb6clfGVRq0K_w5a7Tt6XDb0pqyJxfKif3WLOa1d7vafAIk5fGDyQZj4e6O370duGxBTjcB7V8KmBrdMfQG0vNBORLwTrScGW5iXiSfhWip1kTm2fViZYuVr7uOv3m1PsHmI4J8TwA_CDQ_XDMrIlt1l6-EFVDYm3j81DoM_p0dR4O-S8kUQKSmf_NbbVqZZyvbL9xaW8BXcmsaM7WB3e5p5tN_OAmE4TJ2S5BWNc6e0sIEfAIvSMlXLqvwlPaY4CN4UK73Q2CAXXUns-fEoOWEg'
#         UserToken.create_or_update(token=token, server_with_port=server_with_port)
