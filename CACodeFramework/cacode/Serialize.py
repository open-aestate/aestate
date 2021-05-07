# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        Serialize
# Author:           CACode
# Version:          1.2
# Created:          2021/4/27
# Description:      Main Function:    序列化和反序列化
#                   使用QuerySet[QueryItem]形式存储数据,并通过JsonUtil解析成json
#                   增强版list+dict
# Class List:    JsonUtil -- Json工具集
#               QuerySet -- 返回的结果集对象
#               QueryItem -- 返回的子集对象
# History:
#       <author>        <version>       <time>      <desc>
#       CACode              1.2     2021/4/27    统一序列化器位置
# ------------------------------------------------------------------
import functools
from datetime import date, datetime

from CACodeFramework.cacode import ReviewJson
from CACodeFramework.util.Log import CACodeLog
import _ctypes
from CACodeFramework.cacode.ReviewJson.JSON import Json

__all__ = ['JsonUtil', 'QuerySet', 'QueryItem', 'Page']


class JsonUtil(Json):
    """作者:CACode 最后编辑于2021/4/27
    Json工具
    JsonUtil.parse(**kwargs):将任意对象解析成json字符串
    JsonUtil.load(**kwargs):将字符串解析成字典
    """

    @staticmethod
    def date_encoder(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return None

    class JsonDateEncoder(ReviewJson.JSONEncoder):
        def default(self, obj):
            return JsonUtil.date_encoder(obj)

    class SimplejsonDateEncoder(ReviewJson.JSONEncoder):
        def default(self, obj):
            return JsonUtil.date_encoder(obj)

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
            json_f = functools.partial(JsonUtil.dumps, cls=JsonUtil.JsonDateEncoder)
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
            return JsonUtil.load(result)
        elif bf:
            return JsonUtil.beautiful(JsonUtil.load(result))
        return result

    @staticmethod
    def load(item):
        """作者:CACode 最后编辑于2021/4/27
        将json字符串解析成字典
        """
        if isinstance(item, list):
            _dats = []
            for i in item:
                _dats.append(JsonUtil.load(i))
            return _dats
        elif isinstance(item, tuple):
            # 如果是tuple元组则转成集合后递归
            _dats = []
            for i in list(item):
                _dats.append(JsonUtil.load(i))
            return _dats
        elif isinstance(item, dict):
            # 如果是字典,则直接返回
            return item
        elif isinstance(item, str):
            # 如果是字符串则解析为字典
            return JsonUtil.loads(item)
        elif isinstance(item, object):
            # 如果是object则交给parse_obj()解析
            return item.__dict__
        else:
            return JsonUtil.loads(item)

    @staticmethod
    def beautiful(_data):
        """作者:CACode 最后编辑于2021/4/27
        美化json
        """
        return JsonUtil.dumps(_data, sort_keys=True, indent=4, separators=(',', ':'))


class QuerySet(list):
    """
    执行database operation返回的结果集对象

    此序列化器采用链表形式储存数据,递归搜索子节点

    顺序从左子树开始依次按照索引排列

    元类:
        list

    附加方法:
        first():
            返回结果集对象的第一个数据

        last():
            返回结果集对象的最后一位参数

        page(size):
            按照每一页有size数量的结果分页

        to_json():
            将结果集对象转json字符串

        add_field():
            添加一个字段使得解析过程中不会被移除

        remove_field():
            删除一个字段使得解析过程中不会添加


    Attr

    """

    def __init__(self, instance, base_data: list, query_items=None):
        """
        初始化传入结果集并附加上base_data数据集

        instance:
            序列化的实例对象

        base_data:
            初始化数据源
        """
        list.__init__([])
        self.__instance__ = instance

        self.__using_fields__ = self.__instance__.__fields__
        self.__all_using_fields__ = JsonUtil.parse(obj=self.__instance__, end_load=True)

        self.__ignore_field__ = {}
        self.__append_field__ = {}
        if not query_items:
            for i in base_data:
                self.append(
                    QueryItem(data_item=i, using_fields=self.__using_fields__, append_field=self.__append_field__,
                              ignore_field=self.__ignore_field__))
        else:
            self.extend(query_items)

    def size(self):
        return len(self)

    def first(self):
        """
        取得结果集的第一位参数
        """
        return self[0]

    def last(self):
        """
        取得结果集的最后一位参数
        """
        return self[len(self) - 1]

    def page(self, size):
        """
        将结果集按照指定数目分割
        """
        return list_of_groups(self, size)

    def to_json(self, bf=False):
        """
        将结果集对象转json处理
        :param bf:是否需要美化sql
        """
        result = []
        for i in self:
            result.append(JsonUtil.load(i.to_json()))
        return JsonUtil.parse(result, bf)

    def add_field(self, key, default_value=None):
        """
        添加一个不会被解析忽略的字段
        """
        if key not in self.__append_field__.keys() and \
                key not in self.__using_fields__.keys() and \
                key not in self.__all_using_fields__.keys():

            self.__append_field__[key] = default_value
        else:
            CACodeLog.log(obj=self, msg='`{}` already exists'.format(key))

    def remove_field(self, key):
        """
        添加一个会被解析忽略的字段
        """
        self.__ignore_field__[key] = None


class QueryItem(JsonUtil):
    """
    序列化器的子节点

    此节点处于二叉树的叶子节点,node分布在各个data_dict

    """

    def __init__(self, ignore_field: dict, append_field: dict, data_item: list, using_fields):
        # 忽略和添加字段的对象地址值
        # 调用时从栈钟取出
        self.ignore_field = ignore_field
        self.append_field = append_field
        # 数据初始化的字典
        self.data_item = data_item
        self.data_dict = data_item.__dict__
        # 存在的字段
        self.using_fields = using_fields

    def to_json(self, bf=False):
        """
        将此叶子节点转json处理
        """
        # 从内存地址获取限定对象
        # 将需要的和不需要的合并
        all_fields = dict(self.using_fields, **self.append_field)
        # 将需要忽略的字典从字典中删除
        for i in self.ignore_field.keys():
            if i in all_fields.keys():
                del all_fields[i]

        # 将不存在字段删除
        for i in all_fields.keys():
            if i in self.data_dict.keys():
                all_fields[i] = getattr(self.data_item, i)

        return self.parse(obj=all_fields, bf=bf)

    def to_dict(self):
        """
        将数据集转字典格式
        """
        return JsonUtil.load(self.to_json())

    def add_field(self, key, default_value=None):
        """
        添加一个不会被解析忽略的字段
        """
        if key not in self.append_field.keys() and \
                key not in self.using_fields.keys():

            self.append_field[key] = default_value
        else:
            CACodeLog.log(obj=self, msg='`{}` already exists'.format(key))

    def remove_field(self, key):
        """
        添加一个会被解析忽略的字段
        """
        self.ignore_field[key] = None


def list_of_groups(init_list, size):
    """
    将数据集按照一定数量分组并返回新数组
    """
    lo_groups = zip(*(iter(init_list),) * size)
    end_list = [list(i) for i in lo_groups]
    count = len(init_list) % size
    QuerySet(query_items=init_list[-count:]) if count != 0 else end_list
    return end_list


class Page(list):
    def __init__(self, querySet: list[QuerySet], size: int):
        list.__init__([])
        self.instances = list_of_groups(querySet, size)

    def to_dict(self):
        pass

    def to_json(self):
        return JsonUtil.load(self.to_json())
