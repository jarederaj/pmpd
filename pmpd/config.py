import os
import json
import errno

from utils import Utils
from compat import is_windows
from . import __version__

TOPLEVEL = Utils().git(['rev-parse', '--show-toplevel'])

DEFAULT_CONFIG_DIR = os.environ.get(
    'GIT_PMPD_CONFIG_DIR',
    os.path.expanduser('%s/.pmpd' % (TOPLEVEL))
)


class BaseConfigDict(dict):

    name = None
    helpurl = None
    about = None
    directory = DEFAULT_CONFIG_DIR

    def __init__(self, directory=None, *args, **kwargs):
        super(BaseConfigDict, self).__init__(*args, **kwargs)
        if directory:
            self.directory = directory

    def __getattr__(self, item):
        return self[item]

    def _get_path(self):
        """Return the config file path without side-effects."""
        return os.path.join(self.directory, self.name + '.json')

    @property
    def path(self):
        """Return the config file path creating basedir, if needed."""
        path = self._get_path()
        try:
            os.makedirs(os.path.dirname(path), mode=0o700)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path

    @property
    def is_new(self):
        return not os.path.exists(self._get_path())

    def load(self):
        try:
            with open(self.path, 'rt') as f:
                try:
                    data = json.load(f)
                except ValueError as e:
                    raise ValueError(
                        'Invalid %s JSON: %s [%s]' %
                        (type(self).__name__, e.message, self.path)
                    )
                self.update(data)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise

    def save(self):
        self['__meta__'] = {
            'pmpd': __version__
        }
        if self.helpurl:
            self['__meta__']['help'] = self.helpurl

        if self.about:
            self['__meta__']['about'] = self.about

        self['__meta__']['toplevel'] = TOPLEVEL

        with open(self.path, 'w') as f:
            json.dump(self, f, indent=4, sort_keys=True, ensure_ascii=True)
            f.write('\n')

    def delete(self):
        try:
            os.unlink(self.path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise



class Config(BaseConfigDict):

    name = 'config'
    helpurl = 'http://www.pyscape.com/pmpd'
    about = 'pmpd configuration file'

    DEFAULTS = {
        'implicit_content_type': 'json',
        'default_options': [],
        'branches': {
            'alpha': {
                'user': '',
                'ip': '',
                'toplevel': '',
                'tickets': [],
                'parents': ['beta','predevelop'],
            },
            'beta': {
                'user': '',
                'ip': '',
                'toplevel': '',
                'tickets': [],
                'parents': ['predevelop'],
            },
        },
        'deployments': {
            'predevelop': {
                'user': '',
                'ip': '',
                'toplevel': '',
                'inherits': 'beta',
            },
            'develop': {
                'user': '',
                'ip': '',
                'toplevel': '',
                'inherits': 'predevelop',
            },
            'master': {
                'user': '',
                'ip': '',
                'toplevel': '',
                'inherits': 'develop',
            }
        }
    }

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.update(self.DEFAULTS)
