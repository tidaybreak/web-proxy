import os
import re
import re
import shutil
import hashlib
from urllib.parse import urlparse, unquote
from functools import wraps


def export(export_name=None):
    """
    标识一个export
    :return:
    """

    def wrapper(func):
        func.__name__ = export_name or func.__name__
        func.export = True

        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper



static_res = {'js': {
    'content-type': 'application/javascript'
}, 'css': {
    'content-type': 'text/css;'
}, 'png': {
    'content-type': 'image/png'
}, 'jpg': {
    'content-type': 'image/jpg'
}, 'gif': {
    'content-type': 'image/gif'
}}


def get_cache_file(url, post_data_hash, contain_query=True):
    # return 'no ', 404, None, None, None
    url = urlparse(url)
    query = unquote(url.query)
    query = re.sub(r'[/%":\s]+', '_', query)
    ext = os.path.splitext(url.path)[-1][1:]
    if ext in static_res:
        contain_query = False

    # 参数台长会导致文件名太长
    if len(query) > 200:
        query = hashlib.md5(bytes(query, encoding='utf-8')).hexdigest()

    # 文件路径，是否包含查询参数规则
    if contain_query:
        file_path = f"{os.getcwd()}/cache/{url.hostname}{url.path}/{query}"
        modify_file_path = f"{os.getcwd()}/modify/{url.hostname}{url.path}/{query}"
        if len(query) == 0:
            file_path = file_path + 'index'
            modify_file_path = modify_file_path + 'index'
    else:
        file_path = f"{os.getcwd()}/cache/{url.hostname}{url.path}"
        modify_file_path = f"{os.getcwd()}/modify/{url.hostname}{url.path}"

    if len(post_data_hash) > 0:
        file_path += '-' + post_data_hash
        modify_file_path += '-' + post_data_hash

    if os.path.isfile(modify_file_path):
        file_path = modify_file_path

    # 如果是目录，要移除，可能和之前生成规则冲突
    if os.path.isdir(file_path):
        shutil.rmtree(file_path)
        print(f"error is path:{file_path}")

    if not os.path.isfile(file_path):
        return 'no ' + file_path, 404, {}, None, None

    f = open(file_path, 'rb')
    data = f.read()
    f.close()

    if ext in static_res:
        return file_path, 200, static_res[ext], {}, data
    else:
        sp = "\r\n"
        new_data = data.split(b"\r\n\r\n", 2)
        if len(new_data) != 3:
            sp = "\n"
            new_data = data.split(b"\n\n", 2)
        if len(new_data) == 3:
            str_h = str(new_data[0], encoding='utf-8')
            h = dict()
            if str_h != '':
                h = '{\'' + str_h.replace(sp, "', '").replace(": ", "': '") + '\'}'
                try:
                    h = eval(h)
                except Exception as error:
                    print("error eval:", h, str(error))
            str_c = str(new_data[1], encoding='utf-8')
            c = dict()
            if str_c != '':
                s = str_c.strip(sp).replace(sp, "', '").replace(": ", "': '")
                c = '{\'' + s + '\'}'
                try:
                    c = eval(c)
                except Exception as error:
                    print("error eval:", c, str(error))
            return file_path, h['status_code'], h, c, new_data[2]
    return 'no err' + file_path, 404, {}, None, None


def save_cache_file(url, post_data_hash, data, status_code=200, header={}, cookies={}, contain_query=True):
    url = urlparse(url)
    query = unquote(url.query)
    query = re.sub(r'[/%":\s]+', '_', query)
    url_path = url.path
    if len(url.path) > 0 and url.path[-1] == '/':
        url_path = url.path[:-1]
    file_path = f"{os.getcwd()}/cache/{url.hostname}{url_path}"
    ext = os.path.splitext(file_path)[-1][1:]
    if ext in static_res:
        contain_query = False

    # 参数台长会导致文件名太长
    if len(query) > 200:
        query = hashlib.md5(bytes(query, encoding='utf-8')).hexdigest()

    if contain_query:
        file_path = file_path + '/' + query
        if len(query) == 0:
            file_path = file_path + '/index'
    # else:
    #     file_path = path
    #     path = '/'.join(path.split('/')[:-1])
        # (path, file_path) = os.path.split(path)

    path = '/'.join(file_path.split('/')[:-1])
    if not os.path.exists(path):
        os.makedirs(path)

    if ext in static_res:
        with open(file_path, 'wb') as f:
            f.write(data)
    else:
        str_header = f"status_code: {status_code}\r\n"
        for k, v in header.items():
            str_header += f"{k}: {v}\r\n"
        str_header += "\r\n"

        str_cookies = '\r\n'
        for k, v in cookies.items():
            str_cookies += f"{k}: {v}\r\n"
        str_cookies += "\r\n"

        if len(post_data_hash) > 0:
            file_path += '-' + post_data_hash
        # print(file_path)
        with open(file_path, 'wb') as f:
            f.write(bytes(str_header, encoding='utf-8'))
            f.write(bytes(str_cookies, encoding='utf-8'))
            f.write(data)


pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)


def is_valid_domain(value):
    """
    Return whether or not given value is a valid domain.
    If the value is valid domain name this function returns ``True``, otherwise False
    :param value: domain string to validate
    """
    return True if pattern.match(value) else False
