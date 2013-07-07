"""This module provides the main functionality of git-pmpd.

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

def main(args=sys.argv[1:], env=Environment()):
    """Run the main program and write the output to ``env.stdout``.

    Return exit status code.

    """

    if env.config.default_options:
        args = env.config.default_options + args

    exit_status = ExitStatus.OK

    return exit_status
