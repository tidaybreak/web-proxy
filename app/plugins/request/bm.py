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
    # 头正常是- 这里要求_ access head paras is blank
    if "App-Id" in headers:
        headers["app_id"] = headers["App-Id"]
    if "Access-Token" in headers:
        headers["access_token"] = headers["Access-Token"]
    if "Time-Stamp" in headers:
        headers["time_stamp"] = headers["Time-Stamp"]
    return headers


@export("request_data")
def request_data(data, *args, **kwargs):
    # host = args[0]
    return data
