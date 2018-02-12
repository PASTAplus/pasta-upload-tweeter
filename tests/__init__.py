#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: __init__

:Synopsis:

:Author:
    servilla
  
:Created:
    12/30/17
"""

import logging
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import daiquiri

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + '/tests.log'
daiquiri.setup(level=logging.INFO,
               outputs=(daiquiri.output.File(logfile),))

def main():
    return 0


if __name__ == "__main__":
    main()