#!/usr/bin/python3
import os
import environ

from utils.singleton_class import SingletonMetaClass

class EnvInjecter(metaclass=SingletonMetaClass):
    def __init__(self, env_var_name="DOT_ENV_PATH"):
        self.env = environ.Env()

        DOT_ENV_PATH = self.env.str(env_var_name, default=None)
        if DOT_ENV_PATH:
            self.env.read_env(DOT_ENV_PATH)
            # self._do_inject()
            self._do_inject_v2()

    def _do_inject(self):
        count_injected = 0
        for key, value in self.env.ENVIRON.items():
            os.environ[key] = value
            count_injected += 1
        return count_injected

    def _do_inject_v2(self):
        os.environ = self.env.ENVIRON
        # count_injected = 0
        # for key, value in self.env.ENVIRON.items():
        #     os.environ[key] = value
        #     count_injected += 1
        # return count_injected

def do_tests():
    os.environ['DOT_ENV_PATH'] = r'K:\secrets\envs\job_scraping_local_AWS_DB.env'
    # env_inject = EnvInjecter()
    EnvInjecter("DOT_ENV_PATH")
    assert os.environ.get('AWS_S3_REGION_BUCKET') == 'us-west-2'


    for key, value in os.environ.items():
        print(f"{key}=[{value}]")


if __name__ == '__main__':
    do_tests()
