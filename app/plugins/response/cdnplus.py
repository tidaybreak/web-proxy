# coding:utf-8

__author__ = 'ti'


import csv
import time
import os
import copy
import datetime
import json
import random
import urllib.parse
import sqlite3
from app.utils import export, export_res_local, export_res_filter
from flask import request

file_db = f"{os.getcwd()}/modify/console.cdnplus.cn/db.db"
conn = sqlite3.connect(file_db, check_same_thread=False)
db = conn.cursor()
# db.execute('''CREATE TABLE flow
#        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#        time DATETIME KEY    NOT NULL,
#        `in`            INT     NOT NULL,
#        out            INT     NOT NULL,
#        flow            INT     NOT NULL,
#        visit            INT     NOT NULL,
#        hit            INT     NOT NULL);''')
# db.execute("CREATE UNIQUE INDEX t ON flow (time);")
# conn.commit()
# conn.close()


eval_globals = {
    'true': True,
    'false': False,
    'null': ''
}


@export_res_local("/flow/")
def flow(res_data, *args, **kwargs):
    (full_path, req_data, res_status, res_headers) = args[0]
    file = request.files['file']
    # f = file.read()
    # f_csv = csv.reader(f)
    # headers = next(f_csv)
    # print("上传的文件的名字是："+f.filename)
    # #保存文件
    # #localPath保存文件到磁盘的指定位置
    # #f.save(localPath)

    file_csv = f"{os.getcwd()}/cache/console.cdnplus.cn/flow.csv"
    file.save(file_csv)
    with open(file_csv) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            t = datetime.datetime.strptime(row[0], "%Y/%m/%d %H:%M")
            if row[3] == '':
                row[3] = '0'
            if row[4] == '':
                row[4] = '0'
            if row[5] == '':
                row[5] = '0'
            sql = "REPLACE INTO flow ('time', 'in', 'out', 'flow', 'visit', 'hit') VALUES ('%s', %s, %s, %s, %s, %s);" % (t, row[1], row[2], row[3], row[4], row[5])
            db.execute(sql)
        conn.commit()
    return res_data


# 带宽流量
@export_res_local("/admin/statistic/billing/")
def billing(res_data, *args, **kwargs):
    (full_path, req_data, res_status, res_headers) = args[0]
    if req_data == b'':
        return res_data
    if req_data == b'' and res_data is None:
        return None

    res_data = {
            "state": True,
            "msg": "ok",
            "data": {
                "headers": [{
                    "name": "time",
                    "label": "时间",
                    "sortable": "custom"
                },
                    {
                        "name": "flow_unit",
                        "label": "流量(GB)",
                        "sortable": False
                    },
                    {
                        "name": "max_bandwidth_unit",
                        "label": "最大带宽(Byte)",
                        "sortable": False
                    },
                    {
                        "name": "count",
                        "label": "访问次数",
                        "sortable": "custom"
                    },
                    {
                        "name": "hit_count",
                        "label": "命中率(%)",
                        "sortable": "custom"
                    }],
                "summaries": ["",
                              "",
                              "\u603b\u6570\u636e\u5408\u8ba1",
                              "0\u00a0\u5b57\u8282",
                              "0\u00a0\u5b57\u8282",
                              "",
                              ""],
                "rows": [],
                "paginator": {
                    "page_size": 10,
                    "count": 0,
                    "page_count": 1
                }
            }
        }

    start_time = datetime.datetime.now() - datetime.timedelta(days=30)
    end_time = datetime.datetime.now()
    if "filters" in args[0][1]:
        filters_times = args[0][1]["filters"].split('"')
        time_gte = filters_times[3].replace(' 08:00', '')
        time_lte = filters_times[7].replace(' 08:00', '')
        start_time = datetime.datetime.strptime(time_gte, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(time_lte, "%Y-%m-%d %H:%M:%S")
    total = int((end_time.timestamp() - start_time.timestamp()) / 300)
    if total > 500:
        total = 500

    sql = "SELECT * from `flow` where `time` <= '%s' limit %d" % (end_time, total)
    cursor = db.execute(sql)
    i = 0
    max_bandwidth_unit_total = 0
    count_total = 0
    for row in cursor:
        # data["data"].append([row[1], row[2] / 1000 / 1000 / 1000])
        max_bandwidth_unit_total += row[2]
        count_total += row[5]
        stamp = int(start_time.timestamp()) + i * 300
        res_data["data"]["rows"].append({
            "time": time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp)),
            "flow_unit": row[4],
            "max_bandwidth_unit": row[2],
            "count": row[5],
            "hit_count": row[6]
        })
        i += 1

    res_data["data"]["summaries"][3] = str(max_bandwidth_unit_total) + "(Byte)"
    res_data["data"]["summaries"][4] = str(count_total) + "字节"
    del res_data["data"]["summaries"]

    res_data = json.dumps(res_data)
    return 200, res_headers, bytes(res_data, encoding='utf-8')


@export_res_local("/admin/node/nodeinfo/")
def nodeinfo(res_data, *args, **kwargs):
    (full_path, req_data, res_status, res_headers) = args[0]
    if req_data == b'':
        return res_data
    if res_data is None:
        return None

    try:
        res_data = eval(res_data, eval_globals)
    except Exception as error:
        return res_data

    res_data["data"]["rows"][0]["remarks"] = ""
    res_data["data"]["rows"][0]["is_online"] = '<i class="fa fa-cloud" aria-hidden="true" style="color:#00FF00;font-size:16px;" title="连接正常"></i>'
    res_data["data"]["rows"][0]["ng_status"] = '<i class="fa fa-internet-explorer" aria-hidden="true" style="color:#00FF00;font-size:16px;" title="监控正常"></i>'
    res_data["data"]["rows"][0]["sync"] = '<i class="fa fa-times-circle" aria-hidden="true" style="color:#00FF00;font-size:16px;" title="DNS同步正常"></i>'

    stationname = ["联通节点1", "联通节点2", "移动节点1", "移动节点2", "移动节点1", "移动节点2", "铁通节点1", "铁通节点2", "广电节点1", "广电节点2", "联通节点3"]
    for i in range(10):
        node = copy.deepcopy(res_data["data"]["rows"][0])
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

        res_data["data"]["rows"].append(node)

    res_data = json.dumps(res_data)
    return bytes(res_data, encoding='utf-8')


@export_res_local("/admin/node/nodezone/")
def nodezone(res_data, *args, **kwargs):
    (full_path, req_data, res_status, res_headers) = args[0]
    if req_data == b'':
        return res_data
    try:
        res_data = eval(res_data, eval_globals)
    except Exception as error:
        return res_data
    res_data["data"]["rows"][0]["display_cdn_prefix"] = "cdn209.com.cn"
    res_data = json.dumps(res_data)
    return bytes(res_data, encoding='utf-8')


@export_res_local("/admin/domain/domainsiteinfo/")
def domainsiteinfo(res_data, *args, **kwargs):
    (full_path, req_data, res_status, res_headers) = args[0]
    if req_data == b'':
        return res_data

    try:
        res_data = res_data.replace(b'cdnplus', b'cdn')
        res_data = eval(res_data, eval_globals)
    except Exception as error:
        return res_data

    res_data["data"]["headers"][0]["label"] = "加速类型"
    cdntype = ["静态加速", "动态加速", "文件下载加速", "静态加速", "动态加速", "文件下载加速", "流媒体点播加速", "流媒体直播"]
    i = 0
    for item in res_data["data"]["rows"]:
        item["full_domain"] = cdntype[i]
        i += 1

    data = json.dumps(res_data)
    return bytes(data, encoding='utf-8')


def get_data(url, y="domain", min=100000000, max=900000000, rate=1):
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
            num = 8640
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M")
            increment = int((end_time.timestamp() - start_time.timestamp()) / num)
            for i in range(1, num):
                stamp = int(start_time.timestamp()) + i * increment
                item = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp)), random.randint(min, max)]
                data["data"].append(item)
    elif y == "db":
        if len(start_time) > 0:
            start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H%M")
            end_time = datetime.datetime.strptime(end_time, "%Y%m%d%H%M")
            total = int((end_time.timestamp() - start_time.timestamp()) / 300)
            # sql = "SELECT * from `flow` where `time` >= '%s' and `time` <= '%s'" % (start_time, end_time)
            sql = "SELECT * from `flow` where `time` <= '%s' limit %d" % (end_time, total)
            cursor = db.execute(sql)
            i = 0
            for row in cursor:
                # data["data"].append([row[1], row[2] / 1000 / 1000 / 1000])
                stamp = int(start_time.timestamp()) + i * 300
                value = rate * row[2] * (1 / random.randint(min, max))
                if total > 288 * 7:
                    data["data"].append([time.strftime("%m-%d", time.localtime(stamp)), value])
                elif total > 288:
                    data["data"].append([time.strftime("%d-%d %H", time.localtime(stamp)), value])
                else:
                    data["data"].append([time.strftime("%H:%M", time.localtime(stamp)), value])
                i += 1

    data = json.dumps(data)
    return data


@export_res_local("/statistic/summary/")
def statistic_summary(res_data, *args, **kwargs):
    (full_path, req_data, res_status, res_headers) = args[0]
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
    return 200, res_headers, bytes(data, encoding='utf-8')


@export_res_local("/statistic/flow-bandwidth/")
def statistic_flow_bandwidth(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="db", min=1, max=1, rate=1 / 1000 / 1000 / 1000)
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/node-bandwidth-ranking/")
def statistic_node_bandwidth_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0])
    return bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/node-flow/")
def statistic_node_flow(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="db", min=1, max=1, rate=1234 * (1 / 1000 / 1000 / 1000))
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/domain-bandwidth/")
def statistic_domain_bandwidth(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="db", min=1, max=1, rate=0.03 * (1 / 1000 / 1000 / 1000))
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/source-fail/")
def statistic_node_visit(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y='time', min=90, max=100)
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/node-flow-ranking/")
def statistic_node_flow_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0])
    return bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/node-visit-ranking/")
def statistic_node_visit_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0])
    return bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/node-visit/")
def statistic_node_visit_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0],  y="db", min=5, max=10, rate=1234 * (1 / 1000 / 1000 / 1000))
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/query-domain-ranking/")
def statistic_query_domain_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0])
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/source-data/")
def statistic_source(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y='time')
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/query-domain-url-ranking/")
def statistic_query_domain_url_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="area")
    return bytes(res_data, encoding='utf-8')


# 状态码
@export_res_local("/statistic/query-code/")
def statistic_query_code(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="code")
    return bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/query-code-ranking/")
def statistic_query_code_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="code")
    return bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/query-hit/")
def statistic_query_hit(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="db", min=5, max=10, rate=1 * (1 / 1000 / 1000 / 1000))
    return 200, args[0][3], bytes(res_data, encoding='utf-8')


@export_res_local("/statistic/query-ip-ranking/")
def statistic_query_ip_ranking(res_data, *args, **kwargs):
    res_data = get_data(args[0][0], y="idc")
    return bytes(res_data, encoding='utf-8')


@export_res_local("/admin/cache/eagerloading/")
def eagerloading(res_data, *args, **kwargs):
    if args[0][1] == b'':
        return res_data
    h = args[0][3]
    h['Content-Type'] = 'application/json; charset=utf-8'
    return 200, h, b'{"state": true, "msg": "ok", "data": {"headers": [{"name": "remark", "label": "\u4efb\u52a1\u540d", "min_width": "100px", "align": "center", "sortable": "custom"}, {"name": "url_desc", "label": "\u6e05\u9664URL", "min_width": "250px", "align": "left", "sortable": false}, {"name": "count", "label": "\u5f15\u7528\u6b21\u6570", "min_width": "50px", "align": "center", "sortable": "custom"}, {"name": "updated_time", "label": "\u6700\u540e\u6267\u884c\u65f6\u95f4", "sortable": false}], "rows": [], "paginator": {"page_size": 10, "count": 0, "page_count": 1}}}'


@export_res_local("/admin/cache/purgecache/")
def purgecache(res_data, *args, **kwargs):
    if args[0][1] == b'':
        return res_data
    h = args[0][3]
    h['Content-Type'] = 'application/json; charset=utf-8'
    return 200, h, b'{"state": true, "msg": "ok", "data": {"headers": [{"name": "remark", "label": "\u4efb\u52a1\u540d", "min_width": "100px", "align": "center", "sortable": "custom"}, {"name": "url_desc", "label": "\u6e05\u9664URL", "min_width": "250px", "align": "left", "sortable": false}, {"name": "count", "label": "\u5f15\u7528\u6b21\u6570", "min_width": "50px", "align": "center", "sortable": "custom"}, {"name": "updated_time", "label": "\u6700\u540e\u6267\u884c\u65f6\u95f4", "sortable": false}], "rows": [{"remark": "3333333333333", "count": 5, "url_desc": "<p>http://www.baidu.com</p>", "updated_time": "2021-06-06 20:23:56", "_id": 5040}], "paginator": {"page_size": 10, "count": 1, "page_count": 1}}}'