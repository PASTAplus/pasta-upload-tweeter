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

def mail_me(subject=None, msg=None, to=None):

    # Convert subject and msg to byte array
    subject = ('Subject: ' + subject + '\n').encode()
    try:
        msg = msg.encode()
    except AttributeError:
        pass

    mail_msg = subject + msg
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(properties.GMAIL_NAME, properties.GMAIL_PASSWORD)
        smtpObj.sendmail(properties.GMAIL_NAME, to, mail_msg)
        response = 'Sending email to ' + to + ' succeeded'
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