#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: mimemail

:Synopsis:
    Provide MIME Multipart email support (see: https://realpython.com/python-send-email/)

:Author:
    servilla

:Created:
    4/3/22
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

import daiquiri

import properties


logger = daiquiri.getLogger(__name__)


def send_mail(subject: str, msg: str) -> bool:

    logger.info(f"{str}\n{msg}")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr((properties.FROM_NAME, properties.FROM))
    message["To"] = formataddr((properties.TO_NAME, properties.TO))

    part = MIMEText(msg, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP(properties.RELAY_HOST, properties.RELAY_TLS_PORT) as server:
            server.starttls()
            server.login(properties.RELAY_USER, properties.RELAY_PASSWORD)
            server.sendmail(properties.FROM, properties.TO, message.as_string())
        return True
    except Exception as e:
        logger.error(e)
        return False
