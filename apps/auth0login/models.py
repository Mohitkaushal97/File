from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

# Create your models here.

# from django.contrib.auth.models import User


class User(AbstractUser):
    # See fields: https://docs.djangoproject.com/en/3.0/ref/contrib/auth/
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser
    first_name = CharField(_("First Name of the User"), blank=True, max_length=150)
    last_name = CharField(_("Last Name of the User"), blank=True, max_length=150)
    email = CharField(_("Email Address of the User"), blank=True, max_length=150)


# THIS IS NOT GOOD! As it created migration code in local Python package!!!
# e.g.:
# C:\Users\username\AppData\Roaming\Python\Python37\site-packages\django\contrib\auth\migrations\0012_auto_20200805_1355.py
# field = User._meta.get_field('first_name')
# field.max_length = 254
