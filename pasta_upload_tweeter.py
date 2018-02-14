#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta_upload_tweeter.py

:Synopsis:
    Listen for PASTA data package upload notification and tweet when occurs.
 
:Author:
    servilla

:Created:
    11/11/17
"""

import http
import logging
import os

import daiquiri
from flask import Flask
from flask import request
import requests

from eml import Eml
import mail_me as mm
import properties
import tweet

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + '/pasta_upload_tweeter.log'
daiquiri.setup(level=logging.INFO, outputs=(daiquiri.output.File(logfile),))
logger = daiquiri.getLogger(__name__)


app = Flask(__name__)


def build_pasta_url(package_id=None):
    scope, identifier, revision = package_id.split('.')
    pasta_url = 'https://' + properties.PORTAL + '/nis/mapbrowse?scope=' + \
                scope + '&identifier=' + identifier + '&revision=' + revision
    return pasta_url


def build_tweet_msg(package_id=None, pasta_url=None, title=None):
    msg = 'New EDI data package {pid} ({url}): "{title}"'.format(pid=package_id,
                                                               url=pasta_url,
                                                               title=title)
    if len(msg) > 280:
        trunc_msg = msg[0:279]
        msg = trunc_msg + '\u2026'

    return msg


def get_eml(package_id=None):
    scope, identifier, revision = package_id.split('.')
    url = 'https://' + properties.PASTA + '/package/metadata/eml/' + \
          scope + '/' + identifier + '/' + revision
    r = requests.get(url=url)
    if r.status_code == requests.codes.ok:
        return r.text.encode()
    else:
        raise Exception('Unable to read EML for {pid}'.format(pid=package_id))


@app.route('/tweet', methods=['POST'])
def upload():

    remote_address = request.environ['REMOTE_ADDR']
    if remote_address not in properties.WHITE_LIST:
        msg = 'Request not from a trusted server!\n'
        logger.error('Unknown address: {addr}'.format(addr=remote_address))
        return msg, http.HTTPStatus.BAD_REQUEST

    package_id = request.get_data().decode('utf-8')
    logger.info(
        'Remote address and pid: {addr}, {pid}'.format(addr=remote_address,
                                                       pid=package_id))

    # Package identifier pattern: "scope.identifier.revision"
    if len(package_id.split('.')) == 3:
        try:
            eml = Eml(get_eml(package_id=package_id))
            url = build_pasta_url(package_id=package_id)
            msg = build_tweet_msg(package_id=package_id, pasta_url=url,
                                  title=eml.title)
            logger.info('Tweet message: {msg}'.format(msg=msg))
            status = tweet.tweet_upload(msg=msg)
            logger.info('{status}'.format(status=status))
            subject = 'INFO: ' + __name__ + ' ' + package_id
            mm.mail_me(subject=subject, msg=str(status), to=properties.MAIL_TO)
            return '\n', http.HTTPStatus.OK
        except Exception as e:
            msg = str(e) + '\n'
            logger.error('Unknown error: {e}'.format(e=msg))
            subject = 'ERROR: ' + __name__ + ' ' + package_id
            mm.mail_me(subject=subject, msg=msg, to=properties.MAIL_TO)
            return msg, http.HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        msg = 'Request package identifier not recognized\n'
        logger.error('Unknown request body: {pid}'.format(pid=package_id))
        return msg, http.HTTPStatus.BAD_REQUEST


if __name__ == '__main__':
    # Host must be set to 0.0.0.0 for use other than localhost, and no debug
    app.run(host='0.0.0.0')
