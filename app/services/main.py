# coding:utf-8

__author__ = 'ti'

import re
from app.services.base import BaseService

TAG = re.compile('[^%]*%([^%]+)%[^%]*')


class MainService(BaseService):
    """
    cmdb配置项服务对象
    """

    def __init__(self, app):
        self.model = "main"
        super(MainService, self).__init__(app)

    def hook_full_path(self, full_path, request_args):
        # [表-操作]过滤&加工data
        full_path = self.plugins['request'].get("request_full_path", lambda x, _: x)(full_path, (request_args))
        return full_path

    def hook_request(self, host, headers, data):
        # 不移除有些会返回403 如：https://wechat.gyfyy.com/gy1yqlc/user/Images/doc/007403.jpg
        headers.pop("If-None-Match", None)
        headers.pop("If-Modified-Since", None)

        # [表-操作]过滤&加工data
        headers = self.plugins['request'].get("request_header", lambda x, _: x)(headers, (host))
        data = self.plugins['request'].get("request_data", lambda x, _: x)(data, (host))
        return headers, data

    def response_local(self, path, full_path, req_data, res_status, res_headers, res_cookies, res_data):
        key = "res_local_" + path
        if key not in self.plugins['response']:
            return False, res_status, res_headers, res_cookies, res_data

        result = self.plugins['response'].get("res_local_" + path, lambda x, _: x)(res_data, (full_path, req_data, res_status, res_headers))
        if type(result) == tuple:
            res_status = result[0]
            res_headers = result[1]
            res_data = result[2]
        elif result is None:
            return False, res_status, res_headers, res_cookies, res_data
        else:
            res_data = result
        return True, res_status, res_headers, res_cookies, res_data

    def response_filter(self, path, full_path, req_data, res_status, res_headers, res_cookies, res_data):
        # [表-操作]过滤&加工data
        remove_headers = ["connection",     # 穗康码 sk.gzonline.gov.cn
                          "transfer-encoding",
                          "content-encoding",
                          "content-length",
                          "status_code"]
        remove_list = []
        for k in res_headers:
            lk = k.lower()
            if lk in remove_headers:
                remove_list.append(k)
        for k in remove_list:
            del res_headers[k]

        res_data = self.plugins['response'].get("response_global", lambda x, _: x)(res_data, (full_path, req_data))
        result = self.plugins['response'].get("res_filter_" + path, lambda x, _: x)(res_data, (full_path, req_data, res_status, res_headers))
        if type(result) == tuple:
            res_status = result[0]
            res_headers = result[1]
            res_data = result[2]
        else:
            res_data = result
        return res_status, res_headers, res_cookies, res_data


