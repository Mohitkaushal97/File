#!/usr/bin/env python
import os
import sys
from common.lib.utils.env_vars import EnvInjecter

if __name__ == "__main__":

    # this code copies the content of env file "path_dot_env" to the os.environ
    # So, this is good to pre-populate configuration
    env_path_1 = r'c:\temp\django_stores_test.env'
    env_path_2 = r'/home/ubuntu/envs/django_stores_test.env'
    envfile_filepath = None
    if os.path.isfile(env_path_1):
        envfile_filepath = env_path_1
    elif os.path.isfile(env_path_2):
        envfile_filepath = env_path_2
    elif os.environ.get("DOT_ENV_PATH", None) is not None:
        envfile_filepath = os.environ.get("DOT_ENV_PATH")

    if envfile_filepath is not None:
        # inject environment variables from file
        os.environ['DOT_ENV_PATH'] = envfile_filepath
        EnvInjecter()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # django_job directory.
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, "apps/django_job"))

    execute_from_command_line(sys.argv)
