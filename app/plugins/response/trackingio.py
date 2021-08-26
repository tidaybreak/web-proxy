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


@export("response_global")
def response_global(data, *args, **kwargs):
    try:
        data = str(data, encoding='utf-8')
        data = data.replace('<title>TrackingIO</title>', '<title>昊盟游戏广告智能投放平台</title>')
        data = data.replace('2021 TrackingIO.com All Rights Reserved', '2021 wy2.com All Rights Reserved')
        data = data.replace('京ICP备14021832号', '粤ICP备14021832号')
        data = bytes(data, encoding='utf-8')
    except Exception as error:
        print("response_global:", args[0], " error:", str(error))
    return data


@export("/hook_path")
def hook_path(data, *args, **kwargs):
    # data = data.replace(b'src="https://api.consoleconnect.com', b'src="/api.consoleconnect.com')
    # data = data.replace(b'https\\x3A\\x2F\\x2Fapi.consoleconnect.com', b'\\x2Fapi.consoleconnect.com')

    return data
