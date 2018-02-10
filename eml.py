#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: eml

:Synopsis:
    Utilities for reading and parsing an Ecological Metadata Lanaguage XML file.

:Author:
    servilla

:Created:
    11/12/17
"""

from lxml import etree


class Eml(object):

    def __init__(self, eml=None):
        self.eml = eml
        self.root = etree.fromstring(self.eml)
        self._title = self._get_title()

    def _get_title(self):
        titles = self.root.xpath('//dataset/title')
        for title in titles:
            return title.text

    @property
    def title(self):
        # Collapse to single line and spaces
        title = ' '.join(self._title.split())
        return title