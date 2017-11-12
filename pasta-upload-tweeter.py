#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta-upload-tweeter.py

:Synopsis:
 
:Author:
    servilla

:Created:
    11/11/17
"""

import logging
import http

import daiquiri
from flask import Flask
from flask import request

import properties
import tweet

app = Flask(__name__)

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('pasta-upload-tweeter.py: ' + __name__)


def build_pasta_url(address=None, package_id=None):
    scope, identifier, revision = package_id.split('.')
    client = get_portal_name(address=address)
    pasta_url = 'https://' + client + '/nis/mapbrowse?scope=' + scope + \
                '&identifier=' + identifier + '&revision=' + revision
    return pasta_url


def build_tweet_msg(package_id=None, pasta_url=None):
    msg = 'New EDI data package {pid} in PASTA: {url}'.format(pid=package_id,
                                                              url=pasta_url)
    return msg


def get_portal_name(address=None):
    if address == properties.PACKAGE_D:
        return 'portal-d.lternet.edu'
    elif address == properties.PACKAGE_S:
        return 'portal-s.lternet.edu'
    elif address == properties.PACKAGE:
        return 'portal.lternet.edu'
    return None


@app.route('/upload', methods=['POST', 'GET'])
def upload():

    package = properties.PACKAGE
    package_s = properties.PACKAGE_S
    package_d = properties.PACKAGE_D

    pasta_addresses = [package, package_d, package_s]

    if request.method == 'POST':
        package_id = request.get_data().decode('utf-8')
        remote_address = request.environ['REMOTE_ADDR']
        if remote_address in pasta_addresses and len(package_id.split('.')) == 3:
            url = build_pasta_url(address=remote_address, package_id=package_id)
            msg = build_tweet_msg(package_id=package_id, pasta_url=url)
            status = tweet.tweet_upload(msg=msg)
            logger.info(status)
            return '\n', http.HTTPStatus.OK
        else:
            return 'Bad request\n', http.HTTPStatus.BAD_REQUEST


if __name__ == '__main__':
    app.run(host='0.0.0.0')
