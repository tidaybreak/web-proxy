# coding:utf-8

__author__ = 'ti'

import os
import json
import traceback
from app.loader import load_plugins


class BaseService(object):
    def __init__(self, app):
        # self.serv = ext.serv
        self.plugins = self.load_plugins(app)

    @staticmethod
    def load_plugins(app):
        plugins = {}
        for name in os.listdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")):
            plugins[name] = load_plugins(name, app)
        return plugins
