# #!/usr/bin/env python
# from django_job.users.models import User
# from django.core.management.base import BaseCommand
# from django.utils.translation import gettext_lazy as _
# from allauth.account.models import EmailAddress
#
#
# class Command(BaseCommand):
#     help = _('Setup admin user')
#
#     def add_arguments(self, parser):
#         parser.add_argument(
#             '--username',
#             '-u',
#             type=str,
#             help=_('Set the admin username'),
#             dest='username',
#             action='store',
#             required=False,
#             default='admin',
#         )
#         parser.add_argument(
#             '--password',
#             '-p',
#             type=str,
#             help=_('Set the admin password'),
#             dest='password',
#             action='store',
#             required=True,
#         )
#         parser.add_argument(
#             '--email',
#             '-e',
#             type=str,
#             help=_('Set the admin e-mail'),
#             dest='email',
#             action='store',
#             required=False,
#             default='admin@gmail.com',
#         )
#
#     def handle(self, *args, **options):
#         '''
#         Creates an admin user and sets their auth token.
#         '''
#
#         username = options['username']
#         password = options['password']
#         email = options['email']
#
#         # Create Super user  end
#         user_instances = User.objects.filter(email=email)
#         if user_instances.exists():
#             user_instance = user_instances.first()
#         else:
#             user_instance = User()
#
#         user_instance.username = username
#         user_instance.email = email
#         user_instance.set_password(password)
#         user_instance.is_superuser = True
#         user_instance.is_staff = True
#         user_instance.is_active = True
#         user_instance.is_admin = True
#         user_instance.save()
#
#         email_address_instances = EmailAddress.objects.filter(email=email)
#         if email_address_instances.exists():
#             email_address_instance = email_address_instances.first()
#         else:
#             email_address_instance = EmailAddress()
#         email_address_instance.email = email
#         email_address_instance.verified = True
#         email_address_instance.user_id = user_instance.id
#         email_address_instance.primary = True
#         email_address_instance.save()
#         # Create Super user  end
