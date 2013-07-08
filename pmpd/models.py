import os
import sys
from config import DEFAULT_CONFIG_DIR, Config

class Environment(object):
    """Holds information about the execution context.

    Groups various aspects of the environment in a changeable object
    and allows for mocking.

    """

    config_dir = DEFAULT_CONFIG_DIR
    colors = 256 if '256color' in os.environ.get('TERM', '') else 88
    stdin = sys.stdin
    stdin_isatty = sys.stdin.isatty()
    stdout_isatty = sys.stdout.isatty()
    stderr_isatty = sys.stderr.isatty()

    def __init__(self, **kwargs):
        try:
            assert all(hasattr(type(self), attr)
                    for attr in kwargs.keys())
        except:
            pass
        self.__dict__.update(**kwargs)

    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = Config(directory=self.config_dir)
            if self._config.is_new:
                self._config.save()
            else:
                self._config.load()
        return self._config
