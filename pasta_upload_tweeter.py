#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta_upload_tweeter.py

:Synopsis:
 
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

from eml import Eml
import mail_me as mm
import properties
import tweet

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + '/pasta_upload_tweeter.log'
daiquiri.setup(level=logging.INFO, outputs=(daiquiri.output.File(logfile),))
logger = daiquiri.getLogger(__name__)

app = Flask(__name__)


def build_pasta_url(address=None, package_id=None):
    scope, identifier, revision = package_id.split('.')
    client = get_portal_name(address=address)
    pasta_url = 'https://' + client + '/nis/mapbrowse?scope=' + scope + \
                '&identifier=' + identifier + '&revision=' + revision
    return pasta_url


def build_tweet_msg(package_id=None, pasta_url=None, full_title=None):
    title = ' '.join(full_title.split()) # Collapse to single line and spaces
    msg = 'New EDI data package {pid} ({url}): "{title}"'.format(pid=package_id,
                                                               url=pasta_url,
                                                               title=title)
    if len(msg) > 280:
        trunc_msg = msg[0:279]
        msg = trunc_msg + '\u2026'

    return msg


def get_portal_name(address=None):
    if address == properties.PACKAGE_D:
        return 'portal-d.edirepository.org'
    elif address == properties.PACKAGE_S:
        return 'portal-s.edirepository.org'
    elif address == properties.PACKAGE:
        return 'portal.edirepository.org'
    return None


def get_package_name(address=None):
    if address == properties.PACKAGE_D:
        return 'package-d.lternet.edu'
    elif address == properties.PACKAGE_S:
        return 'package-s.lternet.edu'
    elif address == properties.PACKAGE:
        return 'package.lternet.edu'
    return None


def get_pasta_name(address=None):
    if address == properties.PACKAGE_D:
        return 'pasta-d.lternet.edu'
    elif address == properties.PACKAGE_S:
        return 'pasta-s.lternet.edu'
    elif address == properties.PACKAGE:
        return 'pasta.lternet.edu'
    return None


@app.route('/tweet', methods=['POST'])
def upload():

    pasta_addresses = [properties.PACKAGE,
                        properties.PACKAGE_S,
                        properties.PACKAGE_D]

    remote_address = request.environ['REMOTE_ADDR']
    if remote_address not in pasta_addresses:
        if properties.DEBUG:
            remote_address = properties.PACKAGE_D
        else:
            msg = 'Request not from a PASTA server!\n'
            logger.error('Unknown address: {addr}'.format(addr=remote_address))
            return msg, http.HTTPStatus.BAD_REQUEST

    package_id = request.get_data().decode('utf-8')
    logger.info(
        'Remote address and pid: {addr}, {pid}'.format(addr=remote_address,
                                                       pid=package_id))
    if len(package_id.split('.')) == 3:
        pasta_host = get_pasta_name(address=remote_address)
        try:
            eml = Eml(package_id=package_id, pasta_host=pasta_host)
            eml_title = eml.title
            url = build_pasta_url(address=remote_address, package_id=package_id)
            msg = build_tweet_msg(package_id=package_id, pasta_url=url,
                                  full_title=eml_title)
            logger.info('Tweet message: {msg}'.format(msg=msg))
            status = tweet.tweet_upload(msg=msg)
            logger.info('{status}'.format(status=status))
            mail = mm.mail_me(status='INFO', msg=status, to=properties.MAIL_TO)
            logger.info(mail)
            return '\n', http.HTTPStatus.OK
        except Exception as e:
            msg = str(e) + '\n'
            logger.error('Unknown error: {e}'.format(e=msg))
            mail = mm.mail_me(status='ERROR', msg=msg, to=properties.MAIL_TO)
            logger.info(mail)
            return msg, http.HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        msg = 'Request package identifier not parsable!\n'
        logger.error('Unknown request body: {pid}'.format(pid=package_id))
        return msg, http.HTTPStatus.BAD_REQUEST


if __name__ == '__main__':
    # Host must be set to 0.0.0.0 for use other than localhost, and no debug
    app.run(host='0.0.0.0')
