# -*- utf-8 -*-
# @Time: 2021/5/30 10:17
# @Author: CACode
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
