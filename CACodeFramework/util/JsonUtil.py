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
    def json_to_str(_obj):
        json_f = functools.partial(json.dumps, cls=JsonDateEncoder)
        json_str = json_f(_obj)
        return json_str

    # 如果他是集合并且里面包含的非字典而是object,则将对象转成字典
    if isinstance(obj, list):
        obj_dicts = []
        for i in obj:
            if isinstance(obj, object):
                obj_dict = i.__dict__
                obj_dicts.append(obj_dict)
        obj = obj_dicts
    elif isinstance(obj, object):
        obj = obj.__dict__
    return json_to_str(obj)


if __name__ == '__main__':
    class A(object):
        def __init__(self):
            self.a = 1
            self.b = 1


    class B(object):
        def __init__(self):
            self.a = 1
            self.b = 1


    print(parse(A()))
