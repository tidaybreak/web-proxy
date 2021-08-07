# coding=utf-8


import requests
import hashlib
from flask import Blueprint, request, make_response
from app.ext import serv, app
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
    if len(paths) > 2 and is_valid_domain(paths[1]):
        real_host = paths[1]
        full_path = request.full_path.replace('/' + real_host, '', 1)

    # cookies = {h: request.cookies.get(h) for h in request.cookies}

    # 获取真实请求url
    headers['Host'] = real_host
    # Origin要判断再设置
    if 'Origin' in headers:
        headers['Origin'] = cfg.HTTP + real_host
    headers['Referer'] = headers.get("Referer", '').replace(request.host_url, cfg.HTTP + real_host + '/')
    read_url = cfg.HTTP + real_host + full_path

    # byte或dict
    post_data = b''
    # Post Content-Type一般是 text/plain  application/x-www-form-urlencoded
    hash_data = b''
    if 'Content-Type' in headers:
        if headers['Content-Type'].find('application/x-www-form-urlencoded') >= 0:
            post_data = request.form.to_dict()
            hash_data = bytes(str(post_data), encoding='utf-8')
        else:
            post_data = request.data
            hash_data = request.data
    post_data_hash = ''
    if len(hash_data) > 0:
        post_data_hash = hashlib.md5(hash_data).hexdigest()

    # 忽略参数维度的url
    contain_query = True
    if request.path in cfg.QUERY_PATH:
        contain_query = False

    get_cache = True
    if request.path in cfg.NO_CACHE_READ_PATH:
        get_cache = False
    if len(cfg.NO_CACHE_READ_PATH) == 1 and cfg.NO_CACHE_READ_PATH[0] == "*":
        get_cache = False
    if get_cache:
        cache_file, status_code, header, cookies, data = get_cache_file(read_url, post_data_hash,
                                                                        contain_query=contain_query)
    else:
        cache_file, status_code, header, cookies, data = 'skip ', 404, None, None, None

    # if True:
    if data is None:
        try:
            status_code = 502
            header = {}
            data = b''

            # 不移除有些会返回403 如：https://wechat.gyfyy.com/gy1yqlc/user/Images/doc/007403.jpg
            headers.pop("If-None-Match", None)
            headers.pop("If-Modified-Since", None)
            headers = {**headers, **cfg.REQ_HEADER}
            result = requests.request(request.method, read_url,
                                      data=post_data,
                                      headers=headers,
                                      allow_redirects=False,
                                      timeout=(8, 8))
            cookies = requests.utils.dict_from_cookiejar(result.cookies)
            if result.status_code in cfg.CACHE_CODES:
                save_cache_file(read_url, post_data_hash, result.content,
                                status_code=result.status_code,
                                header=result.headers,
                                cookies=cookies,
                                contain_query=contain_query)
            status_code = result.status_code
            header = result.headers
            data = result.content
        except Exception as error:
            print("error:", read_url, str(error))

    # 改写数据
    data = serv.main.hook_response(request.path, full_path, post_data, data)

    response = make_response(data)
    for k in header:
        lk = k.lower()
        # 穗康码 sk.gzonline.gov.cn
        if lk == "connection":
            continue

        if lk == "transfer-encoding" or lk == "content-encoding":
            continue

        if lk == "content-length" or lk == "status_code":
            continue

        # print(i, k, result.headers.get(k))
        response.headers[k] = header.get(k)

    print(f"info:, {status_code}  {cache_file}  {cookies}")
    # print(f"info:, {status_code}  {read_url}  {cookies}")

    for k, v in cookies.items():
        response.set_cookie(k, v)

    # try:
    #     for k, v in cookies.items():
    #         response.set_cookie(k, v)
    # except Exception as error:
    #     print("error:", cookies)
    # return data
    return response, status_code


@default.route("/other", methods=["GET", "POST"])
def get_header():
    # catch_all return 才会到这里
    return ''
