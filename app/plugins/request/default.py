# coding:utf-8

__author__ = 'ti'


import time
import os
import datetime
import json
import random
import urllib.parse
from app.utils import export
from urllib.parse import urlparse


@export("request_header")
def request_header(headers, *args, **kwargs):
    # headers = {**headers, **cfg.REQ_HEADER}
    # cookie = headers.get("Cookie", '')
    # host = args[0]
    # if cookie.find('sessionid') < 0:
    #     cookie = '''
    #         csrftoken=ylrHlE3qhb1JltCzBpsUe4RHhinOCC7rWFuqKlsjrW1D5FVj4jSuh9UnO8bbZqdW; sessionid=lm622w840dz4mtu5a0ipp58nbcgda8o8; gdpr_settings=%7B%22is_analytics_enabled%22%3Atrue%7D; portal-token=695bd1e252557328784cb8ceb4f34b407a2d5466805908fff907a4124cbb7272; _pk_id.34.dc78=5877540f6fac1ddd.1628494442.1.1628507743.1628494442.; _pk_ses.34.dc78=1; prod-portal-api-socket-id=10.100.8.49; sc.ASP.NET_SESSIONID=; sc.Status=1; _gcl_au=1.1.2113474648.1628501258; plb=c589f7e483a823b6
    #     '''
    #     headers["Cookie"] = cookie.strip()
    return headers


@export("request_data")
def request_data(data, *args, **kwargs):
    # host = args[0]
    return data
