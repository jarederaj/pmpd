import unittest
import tempfile
import shutil

#################################################################
# Utils/setup
#################################################################

from pmpd.models import Environment
from pmpd.core import main
from pmpd.compat import is_windows, is_py26, bytes, str

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

    stdout = env.stdout
    stderr = env.stderr
    try:
        exit_status = main(args=['--traceback'] + list(args), **kwargs)
        if '--download' in args:
            # Let the progress reporter thread finish.
            time.sleep(.5)
    except Exception:
        sys.stderr.write(stderr.read())
        raise
    except SystemExit:
        exit_status = ExitStatus.ERROR

    stdout.seek(0)
    stderr.seek(0)

    output = stdout.read()
    try:
        r = StrResponse(output.decode('utf8'))
    except UnicodeDecodeError:
        r = BytesResponse(output)
    else:
        if COLOR not in r:
            # De-serialize JSON body if possible.
            if r.strip().startswith('{'):
                #noinspection PyTypeChecker
                r.json = json.loads(r)
            elif r.count('Content-Type:') == 1 and 'application/json' in r:
                try:
                    j = r.strip()[r.strip().rindex('\r\n\r\n'):]
                except ValueError:
                    pass
                else:
                    try:
                        r.json = json.loads(j)
                    except ValueError:
                        pass

    r.stderr = stderr.read()
    r.exit_status = exit_status

    return r

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

    def test_init(self):
        r = cli('init')
        print(r)
        self.assertEqual(r, '')

#################################################################
# CLI argument parsing related tests.
#################################################################


#################################################################
# Test execution.
#################################################################

if __name__ == '__main__':
    unittest.main()
