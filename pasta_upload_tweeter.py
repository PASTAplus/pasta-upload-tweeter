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

from flask import Flask
from flask import request

from eml import Eml
import properties
import tweet

app = Flask(__name__)

def build_pasta_url(address=None, package_id=None):
    scope, identifier, revision = package_id.split('.')
    client = get_portal_name(address=address)
    pasta_url = 'https://' + client + '/nis/mapbrowse?scope=' + scope + \
                '&identifier=' + identifier + '&revision=' + revision
    return pasta_url


def build_tweet_msg(package_id=None, pasta_url=None, full_title=None):
    title = full_title.replace('\n', '')
    msg = 'New EDI data package {pid} ({url}): "{title}"'.format(pid=package_id,
                                                               url=pasta_url,
                                                               title=title)
    return msg


def get_portal_name(address=None):
    if address == properties.PACKAGE_D:
        return 'portal-d.lternet.edu'
    elif address == properties.PACKAGE_S:
        return 'portal-s.lternet.edu'
    elif address == properties.PACKAGE:
        return 'portal.lternet.edu'
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
            return msg, http.HTTPStatus.BAD_REQUEST

    package_id = request.get_data().decode('utf-8')
    if len(package_id.split('.')) == 3:
        pasta_host = get_pasta_name(address=remote_address)
        try:
            eml = Eml(package_id=package_id, pasta_host=pasta_host)
            eml_title = eml.title
            url = build_pasta_url(address=remote_address, package_id=package_id)
            msg = build_tweet_msg(package_id=package_id, pasta_url=url, full_title=eml_title)
            tweet.tweet_upload(msg=msg)
            return '\n', http.HTTPStatus.OK
        except Exception as e:
            msg = str(e) + '\n'
            return msg, http.HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        msg = 'Request package identifier is not parsable into scope.identifier.revision!\n'
        return msg, http.HTTPStatus.BAD_REQUEST


if __name__ == '__main__':
    # Host must be set to 0.0.0.0 for use other than localhost, and no debug
    app.run(host='0.0.0.0')
