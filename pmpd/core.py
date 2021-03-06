"""This module provides the main functionality of pmpd.

Invocation flow:

    1. Read, validate and process the input (args, `stdin`).
    2. Read the config files.
    3. Create and send a request to the git server.
    4. Perform invesitigations.
    5. Exit.

"""

import sys
from models import Environment
from . import ExitStatus
from cli import parser

def main(args=sys.argv[1:], env=Environment()):
    """Run the main program and write the output to ``env.stdout``.

    Return exit status code.

    """

    if env.config.default_options:
        args = env.config.default_options + args

    args = parser.parse_args(args=args, env=env)

    return 0
