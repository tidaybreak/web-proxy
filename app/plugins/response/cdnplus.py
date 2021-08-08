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


def get_data(url, y="domain"):
    url = url.replace('[]', '')
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    domains = url.split('&domain%5B%5D=')
    del domains[0]
    domains[-1] = domains[-1].split('&')[0]
    start_time = query['start_time']
    end_time = query['end_time']
    #type = query['type']

    data = {
        "code": 0,
        "message": "",
        "data": [

        ]
    }

    if y == "domain":
        for domain in domains:
            item = [domain, random.randint(100000000, 900000000)]
            data["data"].append(item)
    elif y == "code":
        for code in [200, 301, 404, 500]:
            item = [code, random.randint(1000000, 9000000)]
            data["data"].append(item)
    elif y == "time":
        num = 13
        start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M")
        end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M")
        increment = int((end_time.timestamp() - start_time.timestamp()) / num)
        for i in range(1, num):
            stamp = int(start_time.timestamp()) + i * increment
            item = [time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp)), random.randint(100000000, 900000000)]
            data["data"].append(item)

    data = json.dumps(data)
    return data


@export("/statistic/summary/")
def statistic_summary(data, *args, **kwargs):
    # data = eval(data)

    # data = str(data)

    data = '''{
            "code": 0,
            "message": "",
            "data": {
                "count": 10,
                "hit_rate": "20.00%",
                "max_bindwidth": "320\xa0bps",
                "flow": "0\xa430字节"
            }
        }
    '''

    # content = str(result.content, encoding='utf-8')
    # content = content.replace('友盟', '昊盟')
    # content = bytes(content, encoding='utf-8')
    return bytes(data, encoding='utf-8')


@export("/statistic/domain-bandwidth/")
def statistic_domain_bandwidth(data, *args, **kwargs):
    data = get_data(args[0][0], "time")
    return bytes(data, encoding='utf-8')


@export("/statistic/node-bandwidth-ranking/")
def statistic_node_bandwidth_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/query-domain-ranking/")
def statistic_query_domain_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/query-domain-url-ranking/")
def statistic_query_domain_url_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


# 状态码
@export("/statistic/query-code/")
def statistic_query_code(data, *args, **kwargs):
    data = get_data(args[0][0], y="code")
    return bytes(data, encoding='utf-8')


@export("/statistic/query-code-ranking/")
def statistic_query_code_ranking(data, *args, **kwargs):
    data = get_data(args[0][0], y="code")
    return bytes(data, encoding='utf-8')


@export("/statistic/query-hit/")
def statistic_query_hit(data, *args, **kwargs):
    data = get_data(args[0][0], y="time")
    return bytes(data, encoding='utf-8')


@export("/statistic/query-ip-ranking/")
def statistic_query_ip_ranking(data, *args, **kwargs):
    data = get_data(args[0][0], y="domain")
    return bytes(data, encoding='utf-8')