# coding:utf-8

__author__ = 'ti'


import time
import os
from app.utils import export


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
    data = '''
        {
        "code": 0,
        "message": "",
        "data": [["2021-08-07 17:55",
        10],
        ["2021-08-07 18:00",
        20],
        ["2021-08-07 18:05",
        30],
        ["2021-08-07 18:10",
        40],
        ["2021-08-07 18:15",
        50],
        ["2021-08-07 18:20",
        60],
        ["2021-08-07 18:25",
        20],
        ["2021-08-07 18:30",
        30],
        ["2021-08-07 18:35",
        10],
        ["2021-08-07 18:40",
        40],
        ["2021-08-07 18:45",
        20],
        ["2021-08-07 18:50",
        30],
        ["2021-08-07 18:55",
        40]]
    }
    '''

    return bytes(data, encoding='utf-8')


@export("/statistic/node-bandwidth-ranking/")
def statistic_node_bandwidth_ranking(data, *args, **kwargs):
    data = '''
        {
        "code": 0,
        "message": "",
        "data": [["2021-08-07 17:55",
        10],
        ["2021-08-07 18:00",
        20],
        ["2021-08-07 18:05",
        30],
        ["2021-08-07 18:10",
        40],
        ["2021-08-07 18:15",
        50],
        ["2021-08-07 18:20",
        60],
        ["2021-08-07 18:25",
        20],
        ["2021-08-07 18:30",
        30],
        ["2021-08-07 18:35",
        10],
        ["2021-08-07 18:40",
        40],
        ["2021-08-07 18:45",
        20],
        ["2021-08-07 18:50",
        30],
        ["2021-08-07 18:55",
        40]]
    }
    '''

    return bytes(data, encoding='utf-8')


@export("/statistic/query-domain-ranking/")
def statistic_query_domain_ranking(data, *args, **kwargs):
    data = '''
        {
        "code": 0,
        "message": "",
        "data": [["2021-08-07 17:55",
        10],
        ["2021-08-07 18:00",
        20],
        ["2021-08-07 18:05",
        30],
        ["2021-08-07 18:10",
        40],
        ["2021-08-07 18:15",
        50],
        ["2021-08-07 18:20",
        60],
        ["2021-08-07 18:25",
        20],
        ["2021-08-07 18:30",
        30],
        ["2021-08-07 18:35",
        10],
        ["2021-08-07 18:40",
        40],
        ["2021-08-07 18:45",
        20],
        ["2021-08-07 18:50",
        30],
        ["2021-08-07 18:55",
        40]]
    }
    '''

    return bytes(data, encoding='utf-8')