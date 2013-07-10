import unittest
import tempfile
import shutil

#################################################################
# Utils/setup
#################################################################

from pmpd.models import Environment
from pmpd.core import main
from pmpd.compat import is_windows, is_py26, bytes, str
from pmpd import ExitStatus

from pmpd import input

OK = 'HTTP/1.1 200'
COLOR = '\x1b['

MOCK_TICKETS = [1,2,3,4,5,6]

MOCK_BRANCHES = {
    'testalpha': {
        'user': '',
        'ip': '127.0.0.1',
        'tickets': [1,2],
        'parents': ['testbeta','testpredevelop'],
    },
    'testbeta': {
        'ip': '127.0.0.1',
        'tickets': [3,4],
        'parents': ['testpredevelop'],
    },
}

MOCK_DEPLOYMENTS = {
    'testpredevelop': {
        'user': '',
        'ip': '127.0.0.1',
        'inherits': 'testbeta',
    },
    'testdevelop': {
        'ip': '127.0.0.1',
        'inherits': 'testpredevelop',
    },
    'testmaster': {
        'ip': '127.0.0.1',
        'inherits': 'testdevelop',
    }
}

def mk_config_dir():
    return tempfile.mkdtemp(prefix='pmpd_test_config_dir')

class TestEnvironment(Environment):
    colors = 0
    stdin_isatty = True,
    stdout_isatty = True
    is_windows = False
    _shutil = shutil  # we need it in __del__ (would get gc'd)

    def __init__(self, **kwargs):

        if 'stdout' not in kwargs:
            kwargs['stdout'] = tempfile.TemporaryFile('w+b')

        if 'stderr' not in kwargs:
            kwargs['stderr'] = tempfile.TemporaryFile('w+t')

        self.delete_config_dir = False
        if 'config_dir' not in kwargs:
            kwargs['config_dir'] = mk_config_dir()
            self.delete_config_dir = True

        super(TestEnvironment, self).__init__(**kwargs)

    def __del__(self):
        if self.delete_config_dir:
            self._shutil.rmtree(self.config_dir)

class BytesResponse(bytes):
    stderr = json = exit_status = None

class StrResponse(str):
    stderr = json = exit_status = None

def environment(**kwargs):
    return env


def cli(*args, **kwargs):
    env = kwargs.get('env')
    if not env:
        env = kwargs['env'] = TestEnvironment()
    
    # setup a mock configuration
    toplevel = env.config['__meta__']['toplevel']

    def get_mock(mock, toplevel):
        branches = MOCK_BRANCHES
        for branch_name in branches:
            branches[branch_name]['toplevel'] = toplevel
        return branches

    env.config.branches = get_mock(MOCK_BRANCHES, toplevel)
    env.config.deployments = get_mock(MOCK_DEPLOYMENTS, toplevel)

    try:
        exit_status = main(list(args), **kwargs)
    except SystemExit:
        exit_status = ExitStatus.ERROR

    return exit_status

class BaseTestCase(unittest.TestCase):

    maxDiff = 100000

    if is_py26:
        def assertIn(self, member, container, msg=None):
            self.assertTrue(member in container, msg)

        def assertNotIn(self, member, container, msg=None):
            self.assertTrue(member not in container, msg)

        def assertDictEqual(self, d1, d2, msg=None):
            self.assertEqual(set(d1.keys()), set(d2.keys()), msg)
            self.assertEqual(sorted(d1.values()), sorted(d2.values()), msg)

    def assertIsNone(self, obj, msg=None):
        self.assertEqual(obj, None, msg=msg)

#################################################################
# Low-level tests of utilities for git and bash.
#################################################################


#################################################################
# High-level tests using cli().
#################################################################

class pmpdTest(BaseTestCase):

    def test_help(self):
        r = cli('test --help')


#################################################################
# CLI argument parsing related tests.
#################################################################

class ArgumentParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = input.Parser()


#################################################################
# Test execution.
#################################################################

if __name__ == '__main__':
    unittest.main()
