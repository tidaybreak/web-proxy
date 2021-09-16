# coding:utf-8

__author__ = 'ti'

from app.utils import export


@export("/statistic/flow-bandwidth/")
def statistic_domain_bandwidth(data, *args, **kwargs):
    return False, False


@export("/flow/")
def flow(data, *args, **kwargs):
    return False, False


@export("/statistic/summary/")
def statistic_summary(data, *args, **kwargs):
    return False, False


@export("/admin/cache/eagerloading/")
def eagerloading(data, *args, **kwargs):
    if data == b'':
        return True, True
    return False, False


@export("/admin/cache/purgecache/")
def purgecache(data, *args, **kwargs):
    if data == b'':
        return True, True
    return False, False
