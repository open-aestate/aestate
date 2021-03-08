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
    json_func = functools.partial(json.dumps, cls=JsonDateEncoder)
    json_str = json_func(obj)
    return json_str


if __name__ == '__main__':
    dic = {
        'id': 1,
        'name': 'yehun',
        'date': datetime.now()
    }
    json_func = functools.partial(json.dumps, cls=JsonDateEncoder)
    print(json_func(dic))
    simplejson_func = functools.partial(simplejson.dumps, cls=SimplejsonDateEncoder)
    print(simplejson_func(dic))
