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

import tweet

app = Flask(__name__)

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('pasta-upload-tweeter.py: ' + __name__)

def build_pasta_url(hostname=None, package_id=None):
    scope, identifier, revision = package_id.split('.')
    pasta_url = 'https://' + hostname + '/nis/mapbrowse?scope=' + scope + \
                '&identifier=' + identifier + '&revision=' + revision
    return pasta_url


def build_tweet_msg(package_id=None, pasta_url=None):
    msg = 'New EDI data package {pid} in PASTA: {url}'.format(pid=package_id,
                                                              url=pasta_url)
    return msg

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return 'Testing PASTA upload tweeter!\n'

    if request.method == 'POST':
        package_id = request.get_data().decode('utf-8')
        logger.info(package_id)
        env = request.environ
        host = request.environ['HTTP_HOST']
        url = build_pasta_url(hostname=host, package_id=package_id)
        msg = build_tweet_msg(package_id=package_id, pasta_url=url)
        status = tweet.tweet_upload(msg=msg)
        logger.info(status)
        return '', http.HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run(debug=True)
