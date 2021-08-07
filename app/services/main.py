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

    def hook_response(self, path, full_path, post_data, data):
        # [表-操作]过滤&加工data
        data = self.plugins['response'].get(path, lambda x, _: x)(data, (full_path, post_data))
        return data
