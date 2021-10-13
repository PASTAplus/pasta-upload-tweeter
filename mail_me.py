#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: mail_me

:Synopsis:
    Send email message using verified gmail account
 
:Author:
    servilla

:Created:
    2/10/18
"""

import logging
import smtplib

import daiquiri

import properties

logger = daiquiri.getLogger(__name__)


def mail_me(subject: str = None, msg: str = None, to: tuple = None) -> str:

    # Convert subject and msg to byte array
    body = ('Subject: ' + subject + '\n').encode() + \
           ("To: " + ", ".join(to) + "\n").encode() + \
           ('From: ' + properties.GMAIL_NAME + '\n\n').encode() + \
           (msg + '\n').encode()

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(properties.GMAIL_NAME, properties.GMAIL_PASSWORD)
        smtpObj.sendmail(from_addr=properties.GMAIL_NAME, to_addrs=to, msg=body)
        response = 'Sending email to ' + ", ".join(to) + ' succeeded'
        logger.info(response)
        return response
    except Exception as e:
        response = 'Sending email failed - ' + str(e)
        logger.error(response)
        return response
    finally:
        smtpObj.quit()


def main():
    return 0


if __name__ == "__main__":
    main()