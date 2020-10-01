#!/usr/bin/python3
import os
from collections import defaultdict
import logging

from sentry_sdk.integrations.logging import LoggingIntegration
from utils.singleton_class import SingletonMetaClass

import sentry_sdk
import traceback

class SentryInit(metaclass=SingletonMetaClass):
    def __init__(self, log_level=logging.INFO, max_events_of_type=100):
        pass
        self.max_events_of_type = max_events_of_type
        self.error_to_count = defaultdict(int)

        self.env = None
        self.mode_flask = False
        self.mode_django = False
        self.mode_celery = False

        self.log_level = log_level
        self.sentry_debug = False

    def set_env(self, env):
        self.env = env
        return self

    def set_mode_flask(self):
        self.mode_flask = True
        return self

    def set_mode_django(self):
        self.mode_django = True
        return self

    def set_mode_celery(self):
        self.mode_celery = True
        return self

    def get_env(self, key, default_value):
        if self.env is None:
            return None

        try:
            # this is for environ package, and call "get_value"
            value = self.env.get_value(key, default=default_value)
            return value
        except AttributeError as err:
            # if env was not Injected, it's still the os.environ environment
            # this should succeed
            os.environ.get(key, default_value)
            value = self.env.get_value(key, default=default_value)
            return value


    def init_with_env(self):
        # sentry_debug = self.env.get_str("SENTRY_DEBUG", None)
        sentry_debug = self.get_env("SENTRY_DEBUG", None)
        if sentry_debug is not None and (sentry_debug==True or sentry_debug.lower()=="true" or sentry_debug==1):
            sentry_debug = True
        else:
            sentry_debug = False

        sentry_dsn = self.get_env("SENTRY_DSN", None)
        if sentry_dsn is None:
            print("SentryInit:: SENTRY_DSN is None")
            return False
        else:
            self.init_with_dsn(sentry_dsn, sentry_debug)

    def init_with_dsn(self, sentry_dsn, sentry_debug=False):
        try:
            # https://flask.palletsprojects.com/en/1.1.x/errorhandling/
            list_integrations = []

            try:
                if self.mode_flask:
                    from sentry_sdk.integrations.flask import FlaskIntegration
                    list_integrations += [FlaskIntegration()]
                if self.mode_django:
                    from sentry_sdk.integrations.django import DjangoIntegration
                    list_integrations += [DjangoIntegration()]
                if self.mode_celery:
                    from sentry_sdk.integrations.celery import CeleryIntegration
                    list_integrations += [CeleryIntegration()]
            except Exception as ex:
                logging.error("error initializing sentry: %s" % (str(ex)))

            if self.log_level is not None:
                # SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)
                sentry_logging = LoggingIntegration(
                    level=self.log_level,  # Capture info and above as breadcrumbs
                    event_level=logging.ERROR,  # Send errors as events
                )
                list_integrations += [sentry_logging]

            sentry_sdk.init(sentry_dsn,
                            with_locals=True,
                            integrations=list_integrations,
                            send_default_pii=False,
                            debug=sentry_debug)
            return True
        except Exception as ex:
            print("SentryInit:: error main: %s" % (ex))

        return False

    def increase_and_should_report(self, ex):
        bt = traceback.format_exc()
        self.error_to_count[bt] += 1
        if self.error_to_count[bt] < self.max_events_of_type:
            return True

        print("not exporting ERROR with stack: __%s__" % (bt))
        return False

    def capture_exception(self, ex):
        if self.increase_and_should_report(ex):
            sentry_sdk.capture_exception(ex)
