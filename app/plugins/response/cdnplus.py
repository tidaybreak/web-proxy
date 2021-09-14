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

eval_globals = {
    'true': True,
    'false': False,
    'null': ''
}

@export("/admin/node/nodeinfo/")
def nodeinfo(data, *args, **kwargs):
    try:
        data = eval(data, eval_globals)
    except Exception as error:
        return data

    data["data"]["rows"][0]["remarks"] = ""
    data["data"]["rows"][0]["is_online"] = '<i class="fa fa-cloud" aria-hidden="true" style="color:#00FF00;font-size:16px;" title="连接正常"></i>'
    data["data"]["rows"][0]["ng_status"] = '<i class="fa fa-internet-explorer" aria-hidden="true" style="color:#00FF00;font-size:16px;" title="监控正常"></i>'
    data["data"]["rows"][0]["sync"] = '<i class="fa fa-times-circle" aria-hidden="true" style="color:#00FF00;font-size:16px;" title="DNS同步正常"></i>'

    stationname = ["联通节点1", "联通节点2", "移动节点1", "移动节点2", "移动节点1", "移动节点2", "铁通节点1", "铁通节点2", "广电节点1", "广电节点2", "联通节点3"]
    for i in range(10):
        node = copy.deepcopy(data["data"]["rows"][0])
        node["stationname"] = stationname[i]
        node["node_ip"] = "192.168.100." + str(i + 10)

        mem_usage = str(random.randint(20, 90))
        node["mem_usage"] = '<div style="position:relative; z-index:1; width:100px; text-align:center; background:#01c571; border:#444444 1px solid; ">'
        node["mem_usage"] += mem_usage
        node["mem_usage"] += '%<div style="position:absolute;top: 0;left: 0;background: #88fb45;width: '
        node["mem_usage"] += mem_usage
        node["mem_usage"] += 'px;opacity: 0.6;max-width: 100%;">&nbsp;&nbsp;&nbsp;</div></div>'

        network_usage1 = str(random.randint(100, 300))
        network_usage2 = str(random.randint(100, 300))
        node["network_usage"] = '<div class="" style="list-style: none;padding-left: 2px;"><table><tr style="border:0"><td style="border:0" title="进服务器的带宽">' +\
        network_usage1 + 'Mbps</td><td style="border:0">	&nbsp;/&nbsp;	</td><td style="border:0" title="出服务器的带宽">' +\
        network_usage2 + 'Mbps</td></tr></table></div>'

        data["data"]["rows"].append(node)

    data = json.dumps(data)
    return bytes(data, encoding='utf-8')


@export("/admin/node/nodezone/")
def nodezone(data, *args, **kwargs):
    try:
        data = eval(data, eval_globals)
    except Exception as error:
        return data
    data["data"]["rows"][0]["display_cdn_prefix"] = "cdn209.com.cn"
    data = json.dumps(data)
    return bytes(data, encoding='utf-8')


@export("/admin/domain/domainsiteinfo/")
def domainsiteinfo(data, *args, **kwargs):
    try:
        data = data.replace(b'cdnplus', b'cdn')
        data = eval(data, eval_globals)
    except Exception as error:
        return data

    data["data"]["headers"][0]["label"] = "加速类型"
    cdntype = ["静态加速", "动态加速", "文件下载加速", "静态加速", "动态加速", "文件下载加速", "流媒体点播加速", "流媒体直播"]
    i = 0
    for item in data["data"]["rows"]:
        item["full_domain"] = cdntype[i]
        i += 1

    data = json.dumps(data)
    return bytes(data, encoding='utf-8')


# 带宽流量
@export("/admin/statistic/billing/")
def billing(data, *args, **kwargs):
    try:
        data = eval(data, eval_globals)
    except Exception as error:
        return data

    for item in data["data"]["headers"]:
        if item["label"] == "域名":
            data["data"]["headers"].remove(item)

    for item in data["data"]["headers"]:
        if item["label"] == "流量":
            item["label"] = "流量(GB)"
        elif item["label"] == "最大带宽":
            item["label"] = "最大带宽(GB)"
        elif item["label"] == "命中次数":
            item["label"] = "命中率(%)"

    start_time = datetime.datetime.now() - datetime.timedelta(days=30)
    end_time = datetime.datetime.now()
    if "filters" in args[0][1]:
        filters_times = args[0][1]["filters"].split('"')
        time_gte = filters_times[3].replace(' 08:00', '')
        time_lte = filters_times[7].replace(' 08:00', '')
        start_time = datetime.datetime.strptime(time_gte, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(time_lte, "%Y-%m-%d %H:%M:%S")
    num = int((end_time.timestamp() - start_time.timestamp()) / 86400)
    increment = 86400
    max_bandwidth_unit_total = 0
    count_total = 0
    for i in range(1, num):
        stamp = int(start_time.timestamp()) + i * increment
        max_bandwidth_unit = random.randint(100, 150)
        max_bandwidth_unit_total += max_bandwidth_unit
        hit_count = random.randint(100000, 900000)
        count_total += hit_count
        data["data"]["rows"].append({
            "time": time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp)),
            "flow_unit": random.randint(100 * 1000, 150 * 1000),
            "max_bandwidth_unit": max_bandwidth_unit,
            "count": hit_count,
            "hit_count": random.randint(90, 100)
        })
    data["data"]["summaries"][3] = str(max_bandwidth_unit_total) + "(Byte)"
    data["data"]["summaries"][4] = str(count_total) + "字节"
    del data["data"]["summaries"]

    data = json.dumps(data)
    return bytes(data, encoding='utf-8')


def get_data(url, y="domain", min=100000000, max=900000000):
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
            num = 86400
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M")
            increment = int((end_time.timestamp() - start_time.timestamp()) / num)
            for i in range(1, num):
                stamp = int(start_time.timestamp()) + i * increment
                item = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp)), random.randint(min, max)]
                data["data"].append(item)

    data = json.dumps(data)
    return data


@export("/statistic/summary/")
def statistic_summary(data, *args, **kwargs):
    url = args[0][0].replace('[]', '')
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    start_time = query.get('start_time', (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d%H%M"))
    end_time = query.get('end_time', datetime.datetime.now().strftime("%Y%m%d%H%M"))
    start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M")
    end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M")
    increment = (end_time.timestamp() - start_time.timestamp()) / 86400

    data = {
            "code": 0,
            "message": "",
            "data": {
                "count": int(random.randint(500, 1500) * increment),
                "hit_rate": str(random.randint(90, 99)) + "%",
                "max_bindwidth": str(random.randint(100, 150)) + "GB",
                "flow": str(random.randint(500, 1000)) + "\xa0TB"
            }
        }

    data = json.dumps(data)
    return bytes(data, encoding='utf-8')


@export("/statistic/domain-bandwidth/")
def statistic_domain_bandwidth(data, *args, **kwargs):
    data = get_data(args[0][0], y="time", min=0, max=160)
    return bytes(data, encoding='utf-8')


@export("/statistic/node-bandwidth-ranking/")
def statistic_node_bandwidth_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/node-flow/")
def statistic_node_flow(data, *args, **kwargs):
    data = get_data(args[0][0], y="time", min=10000, max=15000)
    return bytes(data, encoding='utf-8')


@export("/statistic/node-flow-ranking/")
def statistic_node_flow_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/source-fail/")
def statistic_node_visit(data, *args, **kwargs):
    data = get_data(args[0][0], y='time', min=90, max=100)
    return 200, args[0][3], bytes(data, encoding='utf-8')


@export("/statistic/node-visit-ranking/")
def statistic_node_visit_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/node-visit/")
def statistic_node_visit_ranking(data, *args, **kwargs):
    data = get_data(args[0][0], y="time")
    return bytes(data, encoding='utf-8')


@export("/statistic/query-domain-ranking/")
def statistic_query_domain_ranking(data, *args, **kwargs):
    data = get_data(args[0][0])
    return bytes(data, encoding='utf-8')


@export("/statistic/source-data/")
def statistic_source(data, *args, **kwargs):
    data = get_data(args[0][0], y='time')
    return 200, args[0][3], bytes(data, encoding='utf-8')


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
    data = get_data(args[0][0], y="time", min=90, max=100)
    return bytes(data, encoding='utf-8')


@export("/statistic/query-ip-ranking/")
def statistic_query_ip_ranking(data, *args, **kwargs):
    data = get_data(args[0][0], y="idc")
    return bytes(data, encoding='utf-8')