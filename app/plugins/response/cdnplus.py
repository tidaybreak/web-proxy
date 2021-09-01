# coding:utf-8

__author__ = 'ti'


import time
import os
import copy
import datetime
import json
import random
import urllib.parse
from app.utils import export
from urllib.parse import urlparse


@export("/admin/node/nodeinfo/")
def nodeinfo(data, *args, **kwargs):
    globals = {
        'true': True,
        'false': False
    }
    try:
        data = eval(data, globals)
    except Exception as error:
        return data

    data["data"]["rows"][0]["remarks"] = ""
    node = copy.deepcopy(data["data"]["rows"][0])
    data["data"]["rows"].append(node)
    data["data"]["rows"].append(node)
    data["data"]["rows"].append(node)
    data["data"]["rows"][0]["stationname"] = "潮汕联通节点1"
    data["data"]["rows"][1]["stationname"] = "潮汕联通节点2"
    data["data"]["rows"][2]["stationname"] = "潮汕电信节点1"
    data["data"]["rows"][3]["stationname"] = "潮汕移动节点1"

    data = json.dumps(data)
    return bytes(data, encoding='utf-8')


def get_data(url, y="domain"):
    url = url.replace('[]', '')
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    domains = url.split('&domain%5B%5D=')
    if len(domains) > 1:
        del domains[0]
    domains[-1] = domains[-1].split('&')[0]
    start_time = query.get('start_time', '')
    end_time = query.get('end_time', '')
    #type = query['type']

    data = {
        "code": 0,
        "message": "",
        "data": [

        ]
    }

    def takeSecond(elem):
        return elem[1]

    if y == "domain":
        for domain in domains:
            item = [domain, random.randint(100000000, 900000000)]
            data["data"].append(item)
        data["data"].sort(key=takeSecond)
    elif y == "code":
        for code in [200, 301, 404, 500]:
            item = [code, random.randint(1000000, 9000000)]
            data["data"].append(item)
        data["data"].sort(key=takeSecond)
    elif y == "idc":
        for idc in ['中国电信', '中国移动', '中国联通', '中国广电', '中信网络', '教育网', '其他']:
            item = [idc, random.randint(100000000, 900000000)]
            data["data"].append(item)
        data["data"].sort(key=takeSecond)
    elif y == "area":
        for idc in ['河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '台湾省']:
            item = [idc, random.randint(100000000, 900000000)]
            data["data"].append(item)
        data["data"].sort(key=takeSecond)
    elif y == "time":
        if len(start_time) > 0:
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
                "flow": "30字节"
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


@export("/statistic/node-flow/")
def statistic_node_flow(data, *args, **kwargs):
    data = get_data(args[0][0], "time")
    return bytes(data, encoding='utf-8')


@export("/statistic/node-flow-ranking/")
def statistic_node_flow_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/node-visit/")
def statistic_node_visit(data, *args, **kwargs):
    data = get_data(args[0][0], "time")
    return bytes(data, encoding='utf-8')


@export("/statistic/node-visit-ranking/")
def statistic_node_visit_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/query-domain-ranking/")
def statistic_query_domain_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/query-domain-url-ranking/")
def statistic_query_domain_url_ranking(data, *args, **kwargs):
    data = get_data(args[0][0], y="area")
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
    data = get_data(args[0][0], y="idc")
    return bytes(data, encoding='utf-8')