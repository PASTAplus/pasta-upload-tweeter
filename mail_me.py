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

import properties


def mail_me(status='INFO', msg=None, to=None):
    subject = 'Subject: pasta-upload-tweeter ' + status + '...\n'
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(properties.GMAIL_NAME, properties.GMAIL_PASSWORD)
        smtpObj.sendmail(properties.GMAIL_NAME, to, subject + msg)
        smtpObj.quit()
        return 'Sending email to ' + to + ' succeeded'
    except Exception as e:
        return 'Sending email failed - ' + str(e)


def main():
    return 0


if __name__ == "__main__":
    main()