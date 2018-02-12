#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_mail_me

:Synopsis:

:Author:
    servilla
  
:Created:
    2/10/18
"""

import logging
import os
import unittest

import daiquiri

import mail_me as mm
import properties


logger = daiquiri.getLogger(__name__)


class TestMailMe(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mail_me(self):
        status = mm.mail_me(status='INFO', msg='Test', to=properties.MAIL_TO)
        self.assertIn('succeeded', status)


if __name__ == '__main__':
    unittest.main()