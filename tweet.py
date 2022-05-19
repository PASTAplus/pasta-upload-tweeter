#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: tweet

:Synopsis:
 
:Author:
    servilla

:Created:
    11/9/17
"""

import twitter

import properties


def tweet_upload(msg=None):
    consumer_key = properties.CONSUMER_KEY
    consumer_secret = properties.CONSUMER_SECRET
    access_key = properties.ACCESS_KEY
    access_secret = properties.ACCESS_SECRET

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_key,
                      access_token_secret=access_secret)

    status = None
    if not properties.DEBUG:
        status = api.PostUpdate(status=msg, verify_status_length=False)
    return status


def main():
    return 0


if __name__ == "__main__":
    main()
