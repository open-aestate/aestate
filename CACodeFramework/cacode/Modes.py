# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        Modes
# Author:           CACode
# Version:          1.2
# Created:          2021/4/27
# Description:      Main Function:    所有用到的设计模式
#                   此文件内保存可外置的设计模式,用于让那些脑瘫知道我写的框架用了什么设计模式而不是
#                   一遍一遍问我这框架都用了什么设计模式、体现在哪里,我叼你妈
# Class List:    Singleton -- 单例模式
# History:
#       <author>        <version>       <time>      <desc>
#        CACode            1.2         2021/4/27    将设计模式迁移到此文件内
# ------------------------------------------------------------------

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
    def createDbOpera(cls):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = object.__new__(cls)
        return cls.__instance__


class Recursion:
    """
    递归
    """

    @staticmethod
    def find_key_for_dict(data: dict, key: str):
        """
        在字典里重复递归,直到得出最后的值,如果查不到就返回None
        """
        result = None
        for i in data.keys():
            if i == key:
                result = data[key]
                break
            elif isinstance(data[i], dict):
                result = Recursion.find_key_for_dict(data[i], key)
                # 如果在这个字段里找不到对应的键
                if result is None:
                    continue
                else:
                    break
            else:
                continue
        return result
