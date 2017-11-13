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

import logging

import daiquiri
import requests
from lxml import etree

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('eml.py: ' + __name__)


class Eml(object):

    def __init__(self, package_id=None, pasta_host=None):
        self.package_id = package_id
        self.scope, self.identifier, self.revision = package_id.split('.')
        self.pasta_host = pasta_host
        self.eml = self._get_eml().encode()
        self.root = etree.fromstring(self.eml)
        self._title = self._get_title()

    def _get_eml(self):
        url = 'https://' + self.pasta_host + '/package/metadata/eml/' + \
              self.scope + '/' + self.identifier + '/' + self.revision
        eml = None
        try:
            r = requests.get(url=url)
            if r.status_code == requests.codes.ok:
                eml = r.text
        except Exception as e:
            logger.error(e)
        return eml

    def _get_title(self):
        titles = self.root.xpath('//dataset/title')
        for title in titles:
            return title.text

    @property
    def title(self):
        return self._title