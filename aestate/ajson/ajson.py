from datetime import date, datetime

import functools

from simplejson import JSONEncoder, JSONDecoder
from decimal import Decimal

_default_encoder = JSONEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    encoding='utf-8',
    default=None,
    use_decimal=True,
    namedtuple_as_object=True,
    tuple_as_array=True,
    iterable_as_array=False,
    bigint_as_string=False,
    item_sort_key=None,
    for_json=False,
    ignore_nan=False,
    int_as_string_bitcount=None,
)
_default_decoder = JSONDecoder(encoding=None, object_hook=None, object_pairs_hook=None)


class AList(list):
    def __init__(self, value: list):
        list.__init__([])
        if isinstance(value, list) and len(value) > 0:
            for item in value:
                if isinstance(item, dict):
                    self.append(ADict(item))
                elif isinstance(item, list) and len(item) > 0:
                    self.append(AList(item))
                elif isinstance(item, tuple) and len(item) > 0:
                    self.append(AList(list(item)))
                else:
                    self.append(item)


class ADict(dict):

    def __init__(self, data: dict):
        super(ADict).__init__()
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, ADict(value))
                self[key] = ADict(value)
            elif isinstance(value, list) and len(value) > 0:
                setattr(self, key, AList(value))
                self[key] = AList(value)

            elif isinstance(value, tuple) and len(value) > 0:
                setattr(self, key, AList(list(value)))
                self[key] = AList(list(value))

            else:
                setattr(self, key, value)
                self[key] = value


class AJson:
    """
    Json工具
    AJson.parse(**kwargs):将任意对象解析成json字符串
    AJson.load(**kwargs):将字符串解析成字典
    """

    @staticmethod
    def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None,
              encoding='utf-8', default=None, use_decimal=True,
              namedtuple_as_object=True, tuple_as_array=True,
              bigint_as_string=False, sort_keys=False, item_sort_key=None,
              for_json=False, ignore_nan=False, int_as_string_bitcount=None,
              iterable_as_array=False, **kw):
        """
            转json字符串
        """
        if (not skipkeys and ensure_ascii and
                check_circular and allow_nan and
                cls is None and indent is None and separators is None and
                encoding == 'utf-8' and default is None and use_decimal
                and namedtuple_as_object and tuple_as_array and not iterable_as_array
                and not bigint_as_string and not sort_keys
                and not item_sort_key and not for_json
                and not ignore_nan and int_as_string_bitcount is None
                and not kw
        ):
            return _default_encoder.encode(obj)
        if cls is None:
            cls = JSONEncoder
        return cls(
            skipkeys=skipkeys, ensure_ascii=ensure_ascii,
            check_circular=check_circular, allow_nan=allow_nan, indent=indent,
            separators=separators, encoding=encoding, default=default,
            use_decimal=use_decimal,
            namedtuple_as_object=namedtuple_as_object,
            tuple_as_array=tuple_as_array,
            iterable_as_array=iterable_as_array,
            bigint_as_string=bigint_as_string,
            sort_keys=sort_keys,
            item_sort_key=item_sort_key,
            for_json=for_json,
            ignore_nan=ignore_nan,
            int_as_string_bitcount=int_as_string_bitcount,
            **kw).encode(obj)

    @staticmethod
    def loads(s, encoding=None, cls=None, object_hook=None, parse_float=None,
              parse_int=None, parse_constant=None, object_pairs_hook=None,
              use_decimal=False, **kw):
        """
        json转字典
        """
        if (cls is None and encoding is None and object_hook is None and
                parse_int is None and parse_float is None and
                parse_constant is None and object_pairs_hook is None
                and not use_decimal and not kw):
            return _default_decoder.decode(s)
        if cls is None:
            cls = JSONDecoder
        if object_hook is not None:
            kw['object_hook'] = object_hook
        if object_pairs_hook is not None:
            kw['object_pairs_hook'] = object_pairs_hook
        if parse_float is not None:
            kw['parse_float'] = parse_float
        if parse_int is not None:
            kw['parse_int'] = parse_int
        if parse_constant is not None:
            kw['parse_constant'] = parse_constant
        if use_decimal:
            if parse_float is not None:
                raise TypeError("use_decimal=True implies parse_float=Decimal")
            kw['parse_float'] = Decimal
        return cls(encoding=encoding, **kw).decode(s)

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
    def parse(obj, bf=False, end_load=False):
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
            obj = AList(json_data)
        elif isinstance(json_data, tuple):
            obj = AList(list(json_data))
        elif isinstance(json_data, dict):
            obj = ADict(json_data)
        else:
            return None

        return obj
