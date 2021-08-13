from datetime import date, datetime

import functools

from .sim.JSON import Json
from .sim import JSONEncoder


class CanotfList(list):
    def __init__(self, value: list):
        list.__init__([])
        if isinstance(value, list) and len(value) > 0:
            for item in value:
                if isinstance(item, dict):
                    self.append(CanotfDict(item))
                elif isinstance(item, list) and len(item) > 0:
                    self.append(CanotfList(item))
                elif isinstance(item, tuple) and len(item) > 0:
                    self.append(CanotfList(list(item)))
                else:
                    self.append(item)


class CanotfDict(dict):

    def __init__(self, data: dict):
        super(CanotfDict).__init__()
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, CanotfDict(value))
                self[key] = CanotfDict(value)
            elif isinstance(value, list) and len(value) > 0:
                setattr(self, key, CanotfList(value))
                self[key] = CanotfList(value)

            elif isinstance(value, tuple) and len(value) > 0:
                setattr(self, key, CanotfList(list(value)))
                self[key] = CanotfList(list(value))

            else:
                setattr(self, key, value)
                self[key] = value


class AJson(Json):
    """
    Json工具
    AJson.parse(**kwargs):将任意对象解析成json字符串
    AJson.load(**kwargs):将字符串解析成字典
    """

    @staticmethod
    def date_encoder(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return None

    class JsonDateEncoder(JSONEncoder):
        def default(self, obj):
            return AJson.date_encoder(obj)

    class SimplejsonDateEncoder(JSONEncoder):
        def default(self, obj):
            return AJson.date_encoder(obj)

    @staticmethod
    def parse(obj, ignore_name=None, bf=False, end_load=False):
        """作者:CACode 最后编辑于2021/4/27

        将对象转换成字典格式:
            支持:
                dict
                list
                object
                list[object]
                object[list]
                object[list[object]]
                .......

        注意事项:

            bf和end_load同时只能使用一个

            当两者同时存在时,默认使用end_load功能


        :param obj:需要解析的对象
        :param ignore_name: 在对象中放入需要忽略的字段名
        :param bf:是否需要美化json
        :param end_load:是否需要在最后转成字典格式
        """

        def json_to_str(_obj):
            """
            json转字符串
            """
            json_f = functools.partial(
                AJson.dumps, cls=AJson.JsonDateEncoder)
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
                    obj_dicts = parse_dict(_obj.__dict__)
                except AttributeError as e:
                    obj_dicts = _obj
                    # 异常警告，抛出
            return obj_dicts

        def parse_dict(_obj):
            """作者:CACode 最后编辑于2021/4/27
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
        # 最后的解析结果
        result = json_to_str(obj)
        if end_load:
            return AJson.load(result)
        elif bf:
            return AJson.beautiful(AJson.load(result))
        return result

    @staticmethod
    def load(item):
        """作者:CACode 最后编辑于2021/4/27
        将json字符串解析成字典
        """
        if isinstance(item, list):
            _dats = []
            for i in item:
                _dats.append(AJson.load(i))
            return _dats
        elif isinstance(item, tuple):
            # 如果是tuple元组则转成集合后递归
            _dats = []
            for i in list(item):
                _dats.append(AJson.load(i))
            return _dats
        elif isinstance(item, dict):
            # 如果是字典,则直接返回
            return item
        elif isinstance(item, str):
            # 如果是字符串则解析为字典
            return AJson.loads(item)
        elif isinstance(item, object):
            # 如果是object则交给parse_obj()解析
            return item.__dict__
        else:
            return AJson.loads(item)

    @staticmethod
    def beautiful(_data):
        """作者:CACode 最后编辑于2021/4/27
        美化json
        """
        return AJson.dumps(_data, sort_keys=True, indent=4, separators=(',', ':'))

    @staticmethod
    def json_to_object(json_data):
        if isinstance(json_data, list):
            obj = CanotfList(json_data)
        elif isinstance(json_data, tuple):
            obj = CanotfList(list(json_data))
        elif isinstance(json_data, dict):
            obj = CanotfDict(json_data)
        else:
            return None

        return obj
