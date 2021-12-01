# -*- utf-8 -*-
# @Time: 2021/5/30 10:17
# @Author: CACode
import os
import time
from datetime import datetime

from aestate.conf import BASE_ATTR


def conversion_types(val):
    """
    将val的类型转换为字符串并插入array
    """
    if isinstance(val, datetime):
        val = val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def date_format(time_obj=time, fmt='%Y-%m-%d %H:%M:%S') -> str:
    """
    时间转字符串
    :param time_obj:
    :param fmt:
    :return:
    """
    _tm = time_obj.time()
    _t = time.localtime(_tm)
    return time.strftime(fmt, _t)


def time_to_datetime(t_time):
    """
    时间戳转datetime
    """
    try:
        d_time = datetime.fromtimestamp(t_time)
    except OSError as ose:
        return None
    return d_time


def get_static_fields(cls):
    """
    获取类的非默认全局变量
    """
    retD = list(set(dir(cls)).difference(set(BASE_ATTR)))
    return retD


def fullname(o):
    """获取对象的类名"""
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        cls_name = o.__class__.__name__
    else:
        cls_name = module + '.' + o.__class__.__name__

    if cls_name == 'type':
        cls_name = o.__base__.__module__ + '.' + o.__base__.__name__

    return cls_name


def logTupleToText(next_line=True, *content):
    temp = []
    if isinstance(content, str):
        temp.append(content)
    elif isinstance(content, tuple):
        for c in content:
            if isinstance(c, tuple):
                temp.extend(c)
            else:
                temp.append(str(c))
    else:
        temp.append(str(content))
    if next_line:
        temp.append('\n')
    return ''.join([str(_) for _ in temp])


def write(path, *content):
    """
    写出文件
    :param path:位置
    :param content:内容
    :return:
    """
    # 防止有些使用`/`有些用`\\`
    _sep_path = []
    s = path.split('/')
    [_sep_path.extend(item.split('\\')) for item in s]
    _path = ''
    for i in _sep_path:
        _end = _sep_path[len(_sep_path) - 1]
        if i != _end:
            _path += str(i) + os.sep
        else:
            _path += str(i)
        if not os.path.exists(_path):
            if '.' not in i:
                os.makedirs(_path)
    _write_content = logTupleToText(True, *content)
    with open(os.path.join(_path), mode="a", encoding="UTF-8") as f:
        f.write(_write_content)
        f.close()
