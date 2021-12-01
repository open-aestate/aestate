# -*- coding: utf-8 -*- #
from enum import IntEnum
from typing import T


class Replaceable:
    pass


class Singleton:
    """
    使用单例模式
    """

    @staticmethod
    def createFactory(cls):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = cls(cls.modules)
        return cls.__instance__

    @staticmethod
    def createObject(cls):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    @staticmethod
    def println(cls, text):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = object.__new__(cls)
                print(text)


class Recursion:
    """
    递归
    """

    @staticmethod
    def find_key_for_dict(obj_data: dict, target: str):
        """
        在字典里重复递归,直到得出最后的值,如果查不到就返回None
        """

        def parse_list(listData: list, tag: str):
            result_list = []
            if listData is not None:
                if isinstance(listData, list):
                    for i in listData:
                        if isinstance(i, list) or isinstance(i, tuple):
                            rt = parse_list(list(i), tag)
                            if rt:
                                result_list.append(rt)
                        elif isinstance(i, dict):
                            result_list.append(parse_dict(i, tag))
                        else:
                            result_list.append(parse_obj(i, tag))

                elif isinstance(listData, tuple):
                    result_list.append(parse_list(list(listData), tag))

                elif isinstance(listData, dict):
                    result_list.append(parse_dict(listData, tag))
                else:
                    result_list.append(parse_obj(listData, tag))

            else:
                return result_list
            return result_list

        def parse_dict(dictData, tag: str):
            result_dict = []
            if dictData is not None:
                if isinstance(dictData, dict):
                    if tag in dictData.keys():
                        result_dict.append(dictData.get(tag))
                        dictData.pop(tag)
                    for index, value in dictData.items():
                        if isinstance(value, list) or isinstance(value, tuple):
                            result_dict.append(parse_list(list(value), tag))
                        elif isinstance(value, dict):
                            result_dict.append(parse_dict(value, tag))
                        else:
                            result_dict.append(parse_obj(value, tag))
                elif isinstance(dictData, list):
                    result_dict.append(parse_list(list(dictData), tag))

                else:
                    result_dict.append(parse_obj(dictData, tag))
            else:
                return None
            return result_dict

        def parse_obj(objData, tag: str):

            def load(da: dict):
                obj_item_list = []
                obj_item_dict = {}
                for i, v in da.items():
                    if i == tag:
                        result_obj.append(getattr(objData, i))
                        continue
                    if isinstance(v, list):
                        obj_item_list.append(getattr(objData, i))
                    elif isinstance(v, dict):
                        obj_item_dict[i] = v

                result_obj.append(parse_list(obj_item_list, tag))
                result_obj.append(parse_dict(obj_item_dict, tag))

            result_obj = []

            if isinstance(objData, dict):
                result_obj.append(parse_dict(objData, tag))
            elif isinstance(objData, list):
                result_obj.append(parse_list(list(objData), tag))
            else:
                if isinstance(objData, object):
                    if isinstance(objData, str):
                        return None
                    elif isinstance(objData, int):
                        return None
                    elif isinstance(objData, float):
                        return None
                    else:
                        if hasattr(objData, tag):
                            result_obj.append(getattr(objData, tag))
                            load(da=objData.__dict__)
                        else:
                            load(da=objData.__dict__)
            return result_obj

        return parse_obj(obj_data, target)


class DictTemplate(object):
    """
    字典对象模板
    """

    def __init__(self, init_data):
        self.init_data = init_data

    def add(self, key, obj):
        setattr(self, key, obj)


class DictToObject(object):
    """
    将字典转成对象，解决懒得写中括号
    """

    def __init__(self, dict_data):
        baseClass = DictTemplate(dict_data)
        self.dict_data = dict_data
        self.baseNode = baseClass
        self.verification(self.baseNode, self.dict_data)

    @staticmethod
    def conversion(dict_data: dict):
        node = DictToObject(dict_data)
        return node.baseNode

    def verification(self, node: DictTemplate, value):
        """
        验证模块
        """
        node.init_data = value
        if isinstance(value, dict):
            for key, val in value.items():
                if isinstance(val, (dict, list, tuple)):
                    val = self.verification(DictTemplate(val), val)
                node.add(key, val)

        elif isinstance(value, list):
            list_temp = []
            for val in value:
                if isinstance(val, (dict, list, tuple)):
                    val = self.verification(DictTemplate(val), val)
                list_temp.append(val)
            node.add('', list_temp)

        return node


class CaseItem:
    def __init__(self, flag, method, *args, **kwargs):
        self.flag = flag
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return str(self.flag)


class CaseOperaBase:
    def __init__(self, val, method=None, *args, **kwargs):
        self.val = val
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def item(self, val, order) -> object: ...


class Case(CaseOperaBase):

    def __gt__(self, other):
        """
        左边大于右边
        """

        return self

    def __ge__(self, other):
        return int(self.val) <= int(other)

    def __lt__(self, other):
        """
        左边小于右边
        """
        return int(self.val) < int(other)

    def __le__(self, other):
        """
        左边小于等于右边
        """
        return int(self.val) >= int(other)

    def __eq__(self, other):
        """
        等于
        """
        return self.val == other

    def __ne__(self, other):
        """
        不等于
        """
        return self.val != other

    def item(self, val, order):
        order.opera[self.val] = CaseItem(self.val == val, self.method, self.args[0], **self.kwargs)
        return order


class CaseDefault(CaseOperaBase):
    def item(self, val, order):
        # order.opera[self.val] = CaseItem(True, val, *self.args, **self.kwargs)
        return order.end(self.val)


class Switch:
    """
    弥补python没有switch的缺陷
    使用教程：
            from aestate.util.others import Switch,Case,CaseDefault

            base_symbol = lambda x: x + x

            val = 3
        方式1：
            # case(选择性参数,满足条件时执行的方法,当满足条件后中间方法需要的参数)
            source = Switch(Case(val)) + \
                     Case(0, base_symbol, val) + \
                     Case(1, base_symbol, val) + \
                     Case(2, base_symbol, val) + \
                     Case(3, base_symbol, val) + \
                     Case(4, base_symbol, val) + \
                     Case(5, base_symbol, val) + \
                     CaseDefault(lambda: False)
            print(ajson.aj.parse(source, bf=True))
        方式2：
            source = Switch(Case(val)). \
            case(0, base_symbol, val). \
            case(1, base_symbol, val). \
            case(2, base_symbol, val). \
            case(3, base_symbol, val). \
            case(4, base_symbol, val). \
            case(5, base_symbol, val). \
            end(lambda: False)
        print(ajson.aj.parse(source, bf=True))
    """

    def __init__(self, val):
        self.val = val
        self.opera = {}

    def case(self, item, method, *args, **kwargs):
        if item in self.opera.keys():
            raise KeyError(f'`{item}` Already exists in the `case`')

        self.opera[item] = CaseItem(self.val == item, method, *args, **kwargs)
        return self

    def end(self, default_method, *args, **kwargs):
        """
        默认处理函数
        """

        for k, v in self.opera.items():
            if v.flag:
                return v.method(*v.args, **v.kwargs)
        return default_method(*args, **kwargs)

    def __add__(self, other):
        return other.item(self.val, self)


class EX_MODEL(IntEnum):
    SELECT = 0
    UPDATE = 1
