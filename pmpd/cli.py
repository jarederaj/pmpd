from argparse import SUPPRESS
from .input import Parser
from . import __doc__

def _(text):
    """Normalize whitespace."""
    return ' '.join(text.strip().split())

parser = Parser(
    description='%s <http://www.pyscape.com/pmpd>' % __doc__.strip(),
    epilog='Suggestions and bug reports are greatly appreciated:\n'
           'https://github.com/jarederaj/pmpd/issues'
)

###############################################################################
# Positional arguments.
###############################################################################

positional = parser.add_argument_group(
    title='Positional arguments',
    description=_('''
        These arguments come after any flags and in the
        order they are listed here. Only METHOD is
        always required.
    ''')
)

positional.add_argument(
    'method',
    metavar='METHOD',
    default=None,
    help=_('''
        The pmpd method or action to take on
        feature, hotfix, or deployment
        (start, commit, deploy). If this
        argument is omitted, then pmpd
        will throw an error. 
    ''')
)

positional.add_argument(
    'process',
    metavar='PROCESS',
    default=None,
    help=_('''
        The pmpd method to be used for the request
        (init, feature, hotfix, deploy).
        If this argument is omitted, then pmpd
        will throw an error. 
    ''')
)

# TODO: create connections to a ticket system like Track or Redmine.
positional.add_argument(
    'branch',
    metavar='BRANCH',
    default=None,
    help=_('''
        Specifies the branch to be used without
        prefix. Generally it's a good idea to use
        ticket numbers because they will sync up well.
    ''')
)
###############################################################################
# Troubleshooting
###############################################################################

troubleshooting = parser.add_argument_group(title='Troubleshooting')

troubleshooting.add_argument(
    '--help',
    action='help',
    default=SUPPRESS,
    help='Show this help message and exit'
)
