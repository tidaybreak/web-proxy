# coding=utf-8


import requests
import hashlib
import logging
from flask import Blueprint, request, make_response
from app.ext import serv, app
#from app.settings import log

from app.utils import get_cache_file, save_cache_file, is_valid_domain
from app.config import cfg

default = Blueprint('default', __name__)


@app.before_request
def catch_all():
    if request.url.find('hsf/realtime/focusIndicators') < 0:
        # print(url)
        pass

    headers = {h[0]: h[1] for h in request.headers}

    # 处理path 移除一些随机参数
    full_path = request.full_path
    for args in cfg.REMOVE_ARGS:
        val = request.args.get(args)
        if val:
            remove_args = args + '=' + val
            full_path = full_path.replace('&' + remove_args, '')
            full_path = full_path.replace(remove_args, '')

    # 获取真实host host可能在path[1]
    real_host = request.values.get('real_host', cfg.DOMAIN)
    paths = request.path.split('/')
    if len(paths) > 2 and paths[1] in cfg.DOMAIN_PROXY:
        real_host = paths[1]
        full_path = request.full_path.replace('/' + real_host, '', 1)

    # 获取真实请求url
    headers['Host'] = real_host
    # Origin要判断再设置
    if 'Origin' in headers:
        headers['Origin'] = cfg.HTTP + real_host
    headers['Referer'] = headers.get("Referer", '').replace(request.host_url, cfg.HTTP + real_host + '/')
    read_url = cfg.HTTP + real_host + full_path

    # byte或dict
    req_data = b''
    hash_data = b''
    if 'Content-Type' in headers:
        # Post Content-Type一般是 text/plain  application/x-www-form-urlencoded
        if headers['Content-Type'].find('application/x-www-form-urlencoded') >= 0:
            req_data = request.form.to_dict()
            hash_data = bytes(str(req_data), encoding='utf-8')
        else:
            req_data = request.data
            hash_data = request.data
    post_data_hash = ''
    if len(hash_data) > 0:
        post_data_hash = hashlib.md5(hash_data).hexdigest()

    # 改写header data
    headers, post_data = serv.main.hook_request(real_host, headers, req_data)

    # 获取缓存
    get_cache = True
    if request.path in cfg.NO_CACHE_READ_PATH:
        get_cache = False
    if len(cfg.NO_CACHE_READ_PATH) == 1 and cfg.NO_CACHE_READ_PATH[0] == "*":
        get_cache = False
    contain_query = True
    if request.path in cfg.QUERY_PATH:
        contain_query = False
    cache_file, res_status, res_headers, res_cookies, res_data = 'skip ', 502, {}, None, None
    if get_cache:
        cache_file, res_status, res_headers, res_cookies, res_data = get_cache_file(read_url, post_data_hash,
                                                                        contain_query=contain_query)
    if res_data is None:
        # 获取数据
        try:
            result = requests.request(request.method, read_url,
                                      data=req_data,
                                      headers=headers,
                                      allow_redirects=False,
                                      timeout=(8, 8))
            res_cookies = requests.utils.dict_from_cookiejar(result.cookies)
            res_status = result.status_code
            res_headers = {k: result.headers.get(k) for k in result.headers}
            res_data = result.content
            if result.status_code in cfg.CACHE_CODES:
                save_cache_file(read_url, post_data_hash, result.content,
                                status_code=result.status_code,
                                header=result.headers,
                                cookies=res_cookies,
                                contain_query=contain_query)
        except Exception as error:
            res_data = b''
            logging.error("error:%s  rul:%s" % (str(error), read_url))

    # 改写数据
    res_headers, res_data = serv.main.hook_response(request.path, full_path, req_data, res_headers, res_data)

    response = make_response(res_data)
    for k in res_headers:
        response.headers[k] = res_headers.get(k)

    if res_cookies:
        for k, v in res_cookies.items():
            response.set_cookie(k, v)

    print(f"info:, {res_status}  {cache_file}  {res_cookies}")
    # print(f"info:, {status_code}  {read_url}  {cookies}")

    return response, res_status


@default.route("/other", methods=["GET", "POST"])
def get_header():
    # catch_all return 才会到这里
    return ''
