# coding: utf-8

import json

import simplejson
import functools
from datetime import date, datetime
import warnings


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
    """作者:CACode 最后编辑于2021/4/10

    将对象转换成字典格式:
        支持:
            dict
            list
            object
            list[object]
            object[list]
            object[list[object]]
            .......
    Returns:
        返回字典格式
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
            # 循环集合
            if isinstance(item, list):
                # 如果是集合则递归
                obj_dicts.append(parse_list(item))
            elif isinstance(item, tuple):
                # 如果是tuple元组则转成集合后递归
                return obj_dicts.append(parse_list(list(item)))
            elif isinstance(item, dict) or isinstance(item, str):
                # 如果是字典或者字符串,则直接交给obj_dicts填充
                obj_dicts.append(item)
            elif isinstance(item, object):
                # 如果是object则交给parse_obj()解析
                obj_dicts.append(parse_obj(item))
            else:
                obj_dicts.append(item)
        return obj_dicts

    def parse_obj(_obj) -> str:
        """
        夺命循环递递归
        """
        obj_dicts = []
        if isinstance(_obj, dict):
            _dict = _obj.__dict__
            # 如果是list,则交给parse_list(解决)
            for key, item in _dict.items():
                obj_dicts.append({
                    key: parse_list(item)
                })
        elif isinstance(_obj, list):
            # 如果是字典或者字符串,则直接交给obj_dicts填充
            obj_dicts.append(parse_list(_obj))
        # 由于parse_list()中有对于tuple累心的解析,所以不必担心tuple
        elif isinstance(_obj, str):
            # 如果是字典或者字符串,则直接交给obj_dicts填充
            obj_dicts = _obj
        else:
            # 如果不是list类型,则直接解析成字典
            try:
                obj_dicts = _obj.__dict__
            except AttributeError as e:
                obj_dicts = _obj
                # 异常警告，抛出
                warnings.warn_explicit(
                    'CACode:JSON-A conversion exception was caught, and a forced conversion has been performed',
                    category=Warning, filename='', lineno=0)
        return obj_dicts

    def parse_dict(_obj):
        """作者:CACode 最后编辑于2021/4/10
        解析字典格式
        """
        obj_dicts = {}
        if isinstance(_obj, dict):
            for key, value in _obj.items():
                if isinstance(value, list):
                    obj_dicts[key] = parse_list(value)
                elif isinstance(value, dict):
                    obj_dicts[key] = parse_dict(value)
                else:
                    v = parse_obj(value)
                    obj_dicts[key] = v
        return obj_dicts

    # 如果他是集合并且里面包含的非字典而是object,则将对象转成字典
    if isinstance(obj, list):
        obj = parse_list(obj)
    elif isinstance(obj, dict):
        obj = parse_dict(obj)
    elif isinstance(obj, object):
        obj = parse_obj(obj)
    return json_to_str(obj)


def load(item):
    """
    将json字符串解析成字典
    """
    if isinstance(item, list):
        _dats = []
        for i in item:
            _dats.append(load(i))
        return _dats
    elif isinstance(item, tuple):
        # 如果是tuple元组则转成集合后递归
        _dats = []
        for i in list(item):
            _dats.append(load(i))
        return _dats
    elif isinstance(item, dict):
        # 如果是字典,则直接返回
        return item
    elif isinstance(item, str):
        # 如果是字符串则解析为字典
        return json.loads(item)
    elif isinstance(item, object):
        # 如果是object则交给parse_obj()解析
        return item.__dict__
    else:
        return json.loads(item)


def beautiful(_data):
    """
    美化json
    """
    return json.dumps(_data, sort_keys=True, indent=4, separators=(',', ':'))


if __name__ == '__main__':
    a = {
        'a': 1,
        'b': [1, 2, 3],
        'c': {
            'c1': 1,
            'c2': 2,
            'c3': 3,
            'c4': 4
        },
        'd': 1,
        'e': '1',
        'f': datetime.now()
    }
    a = parse(a)
    print(a)
