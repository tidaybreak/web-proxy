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


@export("/hook_path")
def hook_path(data, *args, **kwargs):
    # data = data.replace(b'src="https://api.consoleconnect.com', b'src="/api.consoleconnect.com')
    # data = data.replace(b'https\\x3A\\x2F\\x2Fapi.consoleconnect.com', b'\\x2Fapi.consoleconnect.com')

    return data
