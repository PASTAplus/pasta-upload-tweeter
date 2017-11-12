#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: tweet

:Synopsis:
 
:Author:
    servilla

:Created:
    11/9/17
"""

import logging

import daiquiri
import twitter

import properties

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('tweet.py: ' + __name__)


def tweet_upload(msg=None):
    consumer_key = properties.CONSUMER_KEY
    consumer_secret = properties.CONSUMER_SECRET
    access_key = properties.ACCESS_KEY
    access_secret = properties.ACCESS_SECRET

    if msg is None:
        msg = 'Testing PASTA update tweeter!'

    status = None

    try:
        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_key,
                          access_token_secret=access_secret)
        status = api.PostDirectMessage(text=msg, screen_name='GauchoSays')
    except Exception as e:
        logger.error(e)

    return status


def main():
    return 0


if __name__ == "__main__":
    main()
