#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_mail_me

:Synopsis:

:Author:
    servilla
  
:Created:
    2/10/18
"""

import logging
import os
import unittest

import daiquiri

import mail_me as mm
import properties


logger = daiquiri.getLogger(__name__)


class TestMailMe(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mail_me(self):
        msg = '\n{"created_at": "Wed Feb 14 03:53:40 +0000 2018", "hashtags": [], "id": 963622241467379712, "id_str": "963622241467379712", "lang": "en", "source": "<a href=\"https://github.com/EDIorg/pasta-upload-tweeter\" rel=\"nofollow\">PASTA-upload-tweeter</a>", "text": "New EDI data package knb-lter-sbc.6003.2 (https://t.co/BRO6fWzo6G): \"SBC LTER: Ocean: Time-series: Mid-water SeaFET\u2026 https://t.co/mLLUKk1U4k", "truncated": true, "urls": [{"expanded_url": "https://portal.edirepository.org/nis/mapbrowse?scope=knb-lter-sbc&identifier=6003&revision=2", "url": "https://t.co/BRO6fWzo6G"}, {"expanded_url": "https://twitter.com/i/web/status/963622241467379712", "url": "https://t.co/mLLUKk1U4k"}], "user": {"created_at": "Fri Oct 20 17:48:34 +0000 2017", "description": "The Environmental Data Initiative accelerates the curation and archive of environmental data.", "favourites_count": 67, "followers_count": 83, "friends_count": 41, "id": 921432972024311808, "lang": "en", "listed_count": 1, "name": "EDI", "profile_background_color": "000000", "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "profile_image_url": "http://pbs.twimg.com/profile_images/921444714867503104/BqTW_-Xz_normal.jpg", "profile_link_color": "FF691F", "profile_sidebar_fill_color": "000000", "profile_text_color": "000000", "screen_name": "EDIgotdata", "statuses_count": 642, "time_zone": "Pacific Time (US & Canada)", "url": "https://t.co/jkFyuFnspV", "utc_offset": -28800}, "user_mentions": []}'
        status = mm.mail_me(subject='INFO: '+__name__, msg=msg,
                            to=properties.MAIL_TO)
        self.assertIn('succeeded', status)


if __name__ == '__main__':
    unittest.main()