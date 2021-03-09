# coding: utf-8

import json
import simplejson
import functools
from datetime import date, datetime


def date_encoder(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        return None


class JsonDateEncoder(json.JSONEncoder):
    def default(self, obj):
        return date_encoder(obj)


class SimplejsonDateEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        return date_encoder(obj)


def parse(obj):
    """
    将对象转换成json字符串:
        支持:
            dict
            list
            object
            list[object]
            object[list]
            object[list[object]]
            .......
    """

    def json_to_str(_obj):
        """
        json转字符串
        """
        json_f = functools.partial(json.dumps, cls=JsonDateEncoder)
        json_str = json_f(_obj)
        return json_str

    def parse_list(list_obj):
        """
        解析list数据的json
            放置了递归函数,所以不必担心解析报错或者解析不到位
        """
        obj_dicts = []
        for item in list_obj:
            if isinstance(item, list):
                obj_dicts.append(parse_list(item))
            elif isinstance(item, object):
                obj_dict = item.__dict__
                obj_dicts.append(obj_dict)
        return obj_dicts

    # 如果他是集合并且里面包含的非字典而是object,则将对象转成字典
    if isinstance(obj, list):
        obj = parse_list(obj)
    elif isinstance(obj, object) and not isinstance(obj, dict):
        obj = obj.__dict__
    return json_to_str(obj)


def load(obj: str or dict):
    """
    将json字符串解析成字典
    """
    if isinstance(obj, object) and not isinstance(obj, dict):
        return obj.__dict__
    return json.loads(obj)


if __name__ == '__main__':
    class A(object):
        def __init__(self):
            self.a = 1
            self.b = 1


    class B(object):
        def __init__(self):
            self.a = 1
            self.b = 1


    C = {"a": 1, "b": 1}

    print(load(A()))
