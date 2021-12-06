# -*- coding: utf-8 -*- #
__author__ = 'CACode'

from aestate.ajson import aj

"""
此文件内包含有序列化器所有需要用到的参数
aj可使用原simplejson部分功能，内嵌simplejson，升级功能包含
- parse(obj,bf,end_load) 解析object类型
- load(obj) 生成字典
"""

__all__ = ['aj', 'QuerySet', 'PageHelp']


class QuerySet(list):
    """
    执行database operation返回的结果集对象

    此序列化器采用链表形式储存数据,递归搜索子节点

    顺序从左子树开始依次按照索引排列

    元类:
        list

    Methods:
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

        get():
            返回指定位置的参数

    Attribute:

        instance:实例类型模板

        base_data:基本数据

        query_item:使用已有的数据生成QuerySet对象

    """

    def __init__(self, instance=None, base_data=None, query_items=None):
        """
        初始化传入结果集并附加上base_data数据集

        instance:
            序列化的实例对象

        base_data:
            初始化数据源
        """
        list.__init__([])
        if query_items is None:
            self.__instance__ = instance
            # 合并结果集对象
            self.extend(base_data)
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
        return PageHelp.list_of_groups(init_list=self, size=size)

    def to_json(self, bf=False):
        """
        将结果集对象转json处理
        :param bf:是否需要美化sql
        """
        result = []
        for i in self:
            result.append(aj.load(i.to_json(bf=bf)))
        return aj.parse(result, bf=bf)

    def to_dict(self):
        result = []
        for i in self:
            result.append(aj.load(i.to_dict()))
        return result

    def add_field(self, key, default_value=None):
        """
        添加一个不会被解析忽略的字段
        """

        [self[i].add_field(key, default_value) for i in range(len(self))]

    def remove_field(self, key):
        """
        添加一个会被解析忽略的字段
        """
        [self[i].remove_field(key) for i in range(len(self))]

    def get(self, index):
        """
        返回指定位置的元素
        """
        return self[index]


class PageHelp(list):
    def __init__(self, init_data: list):
        list.__init__([])

        self.__dict_data__ = {}
        self.__json_data__ = ""

        self.extend(init_data)

    def to_dict(self):
        """
        节省资源
        """
        if not self.__dict_data__:
            self.__dict_data__ = aj.load(self.to_json())
        return self.__dict_data__

    def to_json(self, bf=False):
        """
        节省资源
        """
        if not self.__json_data__:
            json_str = [i.to_dict() for i in self]
            self.__json_data__ = aj.parse(json_str, bf)
        return self.__json_data__

    @classmethod
    def list_of_groups(cls, init_list, size):
        """
        将数据集按照一定数量分组并返回新数组
        """
        list.__init__([])
        lo_groups = zip(*(iter(init_list),) * size)
        end_list = [QuerySet(query_items=i) for i in lo_groups]
        count = len(init_list) % size
        end_list.append(QuerySet(
            query_items=init_list[-count:])) if count != 0 else QuerySet(query_items=end_list)
        return PageHelp(end_list)

    def get(self, index):
        return self[index]
