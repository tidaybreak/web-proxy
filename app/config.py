# coding:utf-8

import os


__author__ = 'Ti'

basedir = os.path.abspath(os.path.dirname(__file__))


class TraceMixinConfig:
    """
    用来映射trace流程模板中render详细信息的字典，不在这里配置的字典将会默认映射到common
    """

    def __init__(self):
        pass

    pass


class Config(TraceMixinConfig):
    PORT = 5000
    DOMAIN = 'console.cdnplus.cn'
    HTTP = "https://"
    APPLICATION_ROOT = ""

    # 不缓存的path
    NO_CACHE_READ_PATH = ["*"]

    # 忽略参数维度的url
    QUERY_PATH = []

    # 缓存指定状态
    CACHE_CODES = [200]

    # 移除特定参数 一般移除随机数用
    REMOVE_ARGS = []

    # 请求后端时追加特定头
    REQ_HEADER = {

    }


class WaterConfig(TraceMixinConfig):
    PORT = 5005
    DOMAIN = 'bs08bw.axshare.com'
    HTTP = "https://"
    CACHE_CODES = [200]
    # 移除特定参数 一般移除随机数用
    REMOVE_ARGS = []
    REMOVE_HEADER = []
    # 请求后端时追加特定头
    REQ_HEADER = {

    }


# http://game.wy2.com/platform/5f6d566180455950e496e0e7/real/overview
class GameConfig(Config):
    PORT = 5001
    DOMAIN = 'mobile.umeng.com'
    HTTP = "https://"
    CACHE_CODES = [200]
    REMOVE_ARGS = []
    REQ_HEADER = {
        "Cookie": "EGG_SESS=LlHPEAmnR0ZYHqf5ZIizrQq8EW-9J035QBhENQT7S6fNLcNY0nz_N074xTjtKFgNzdPUwdapaqYYagEoKhyEGYn2MCIYsAsp4xOgeOnqF1M=; XSRF-TOKEN-HAITANG=f9079e76-822e-491d-a9ce-5137cc9a6c95; XSRF-TOKEN=32fe8df9-d9cf-4525-9630-2177c71e8ee8; cna=9/coGXOuhT0CAXkuGQPlyKfW; isg=BPX1qqCT-RbvVx2q67KVrVLhB3GvcqmEQQ7z-3ca82y7ThdAP8OAVSKImJL4FcE8; cn_1259864772_dplus=1%5B%7B%7D%2Cnull%2Cnull%2Cnull%2Cnull%2C%22%24direct%22%2C%221797900b6771b6-0f211a0c5341c5-4c3f2c72-1fa400-1797900b678145%22%2C%221621228905%22%2C%22%24direct%22%2C%22%24direct%22%5D; UM_distinctid=1797900b6771b6-0f211a0c5341c5-4c3f2c72-1fa400-1797900b678145; dplus_cross_id=1797900b67b257-04d9973aced9878-4c3f2c72-1fa400-1797900b67c1c8; dplus_finger_print=941813211; cn_1273967994_dplus=1%5B%7B%7D%2Cnull%2Cnull%2Cnull%2Cnull%2C%22%24direct%22%2C%221797900b6771b6-0f211a0c5341c5-4c3f2c72-1fa400-1797900b678145%22%2C%221621228905%22%2C%22%24direct%22%2C%22%24direct%22%5D; CNZZDATA1259864772=990418473-1621228905-%7C1621228905; xlly_s=1",
        "x-xsrf-token-haitang": "f9079e76-822e-491d-a9ce-5137cc9a6c95",
        "X-XSRF-TOKEN": "32fe8df9-d9cf-4525-9630-2177c71e8ee8"
    }


# http://ad.wy2.com/demo.html
class AdConfig(Config):
    PORT = 5002
    DOMAIN = 'www.trackingio.com'
    HTTP = "https://"
    CACHE_CODES = [200]
    REMOVE_ARGS = ["r"]


# http://man.wy2.com/admin/index/index
class HnputihdConfig(Config):
    PORT = 5003
    DOMAIN = 'kptcenter.hnputihd.com'
    HTTP = "http://"
    CACHE_CODES = [200]


# http://man.wy2.com/index.php?c=apps#/appList?_k=sqka55
class ApptrackConfig(Config):
    PORT = 5004
    DOMAIN = 'apptrack.umeng.com'
    HTTP = "https://"
    CACHE_CODES = [200]


env = os.getenv('APP_CONFIG', "")
cfg = globals()['%sConfig' % env]
