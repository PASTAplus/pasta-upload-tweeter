#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_eml

:Synopsis:

:Author:
    servilla
  
:Created:
    12/30/17
"""

import unittest

import daiquiri
from eml import Eml


logger = daiquiri.getLogger(__name__)


class TestEml(unittest.TestCase):
    eml = None

    @classmethod
    def setUpClass(cls):
        with open('./knb-lter-nin.1.1.xml', 'r') as f:
            xml = f.read().encode()
        TestEml.eml = Eml(eml=xml)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_title(self):
        title = 'Daily Water Sample Nutrient Data for North Inlet Estuary, ' \
                'South Carolina, from 1978 to 1992, North Inlet LTER'
        eml_title = TestEml.eml.title
        self.assertEqual(title, eml_title)


if __name__ == '__main__':
    unittest.main()