from flask import Flask, request, jsonify, Response, make_response
import requests
from units import get_cache_file, save_cache_file, is_valid_domain
from config import cfg
import hashlib
import logging
import sys, getopt
import re

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    return app


app = create_app()

# 忽略参数的url
query_urls = []
cache_code = [200, 302]


@app.before_request
def proxy():
    headers = {h[0]: h[1] for h in request.headers}
    url = request.url
    real_host = request.values.get('real_host', cfg.DOMAIN)
    real_full_path = request.full_path

    # 移除一些随机参数
    for args in cfg.REMOVE_ARGS:
        val = request.args.get(args)
        if val:
            remove_args = args + '=' + val
            real_full_path = real_full_path.replace('&' + remove_args, '')
            real_full_path = real_full_path.replace(remove_args, '')

    # 如果第一个是域名
    paths = request.path.split('/')
    if len(paths) > 2 and is_valid_domain(paths[1]):
        real_host = paths[1]
        real_full_path = request.full_path.replace('/'+real_host, '', 1)

    if url.find('hsf/realtime/focusIndicators') < 0:
        # print(url)
        pass

    # cookies = {h: request.cookies.get(h) for h in request.cookies}

    host_url = cfg.HTTP + real_host
    headers['Host'] = real_host
    # Origin要判断再设置
    if 'Origin' in headers:
        headers['Origin'] = host_url
    headers['Referer'] = headers.get("Referer", '').replace(request.host_url, host_url + '/')
    p_url = host_url + real_full_path

    contain_query = True
    if request.path in query_urls:
        contain_query = False

    post_data = request.data

    # Post Content-Type一般是 text/plain  application/x-www-form-urlencoded
    post_data_byte = b''
    if 'Content-Type' in headers:
        if headers['Content-Type'].find('application/x-www-form-urlencoded') >= 0:
            post_data = request.form.to_dict()
            post_data_byte = bytes(str(post_data), encoding='utf-8')
        else:
            post_data_byte = request.data
    post_data_hash = ''
    if len(post_data_byte) > 0:
        post_data_hash = hashlib.md5(post_data_byte).hexdigest()

    cache_file, status_code, header, cookies, data = get_cache_file(p_url, post_data_hash, contain_query=contain_query)

    #if True:
    if data is None:
        try:
            status_code = 502
            header = {}
            data = b''

            # 不移除有些会返回403 如：https://wechat.gyfyy.com/gy1yqlc/user/Images/doc/007403.jpg
            headers.pop("If-None-Match", None)
            headers.pop("If-Modified-Since", None)
            headers = {**headers, **cfg.REQ_HEADER}
            result = requests.request(request.method, p_url,
                                      data=post_data,
                                      headers=headers,
                                      allow_redirects=False,
                                      timeout=(8, 8))
            cookies = requests.utils.dict_from_cookiejar(result.cookies)
            if result.status_code in cfg.CACHE_CODES:
                save_cache_file(p_url, post_data_hash, result.content,
                                status_code=result.status_code,
                                header=result.headers,
                                cookies=cookies,
                                contain_query=contain_query)
            status_code = result.status_code
            header = result.headers
            data = result.content
        except Exception as error:
            print("error:", p_url, str(error))

    # content = str(result.content, encoding='utf-8')
    # content = content.replace('友盟', '昊盟')
    # content = bytes(content, encoding='utf-8')
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
    # print(f"info:, {status_code}  {p_url}  {cookies}")

    for k, v in cookies.items():
        response.set_cookie(k, v)

    # try:
    #     for k, v in cookies.items():
    #         response.set_cookie(k, v)
    # except Exception as error:
    #     print("error:", cookies)
    # return data
    return response, status_code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=cfg.PORT)
    # app.run(host='0.0.0.0', port=443, ssl_context=('keys/secret.pem', 'keys/secret.key'))
