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


@export("request_full_path")
def request_full_path(full_path, *args, **kwargs):
    return full_path


@export("request_header")
def request_header(headers, *args, **kwargs):
    # headers = {**headers, **cfg.REQ_HEADER}
    cookie = headers.get("Cookie", '')
    host = args[0]
    # if cookie.find('sessionid') < 0:
    cookie = '''
            csrftoken=dcSlUdT6earKwkzUc5ECMCnbtsOHAKSnpImKq04HBiUqLIoyBDKzY5uVIXgwfD2g; sessionid=im49qcrdd6hvwcdi4tbw61qqo3id0qll; Hm_lvt_2255d7f5bf3b62859fedb3023aab988c=1631773420; Hm_lpvt_2255d7f5bf3b62859fedb3023aab988c=1631773420
        '''
    headers["Cookie"] = cookie.strip()
    return headers


@export("request_data")
def request_data(data, *args, **kwargs):
    # host = args[0]
    return data
