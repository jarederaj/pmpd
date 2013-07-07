#!/usr/bin/env python
""" The main entry point. Invoke as `git-pmpd' or `python -m git-pmpd'.

"""

import sys
from core import main


if __name__ == '__main__':
    sys.exit(main())
