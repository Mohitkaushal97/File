import time
from timeit import default_timer


class MyTimer(object):
    def __init__(self, description, logger, verbose=True):
        self.description = description
        self.verbose = verbose
        self.timer = default_timer
        self.logger = logger

    def __enter__(self):
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs
        # self.elapsed = self.elapsed_secs
        if self.verbose:
            self.logger.info('** done task %s ; elapsed %2.5f ms' % (self.description, self.elapsed))
