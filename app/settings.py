# coding=utf-8

import json
import sys
import time
import logging
import traceback
from flask import Flask
from app.ext import init_ext


def create_app(conf=None):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    init_ext(app)
    return app


def configure_blueprints(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)
    return app


