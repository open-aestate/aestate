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
import functools


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
    def find_key_for_dict(dictData: dict, target: str, notFound: object):
        """
        在字典里重复递归,直到得出最后的值,如果查不到就返回None
        """

        queue = [dictData]
        result = []
        while len(queue) > 0:
            data = queue.pop()
            for key, value in data.items():
                if key == target:
                    result.append(value)
                elif type(value) == dict:
                    queue.append(value)
        if not result:
            result = notFound
        return result

        # cp_data = data
        #
        # serializer_data = JsonUtil.parse(cp_data, end_load=True)
        #
        # result = None
        # if key in serializer_data.keys():
        #     return f"{cp_data.__class__.__name__}.{key}"
        # for i in serializer_data.keys():
        #     if isinstance(serializer_data[i], dict):
        #         result = Recursion.find_key_for_dict(cp_data[i], key)
        #         # 如果在这个字段里找不到对应的键
        #         if result is None:
        #             continue
        #         else:
        #             break
        #     else:
        #         continue
        #
        # rep_list = str(result).split('.')
        # obj = data
        # for i in rep_list:
        #     if hasattr(obj, i):
        #         obj = getattr(obj, i)
        # return result

    class Replaceable:
        pass

    @staticmethod
    def dict_to_object(data: dict, instance=Replaceable):
        """
        将字典转换为对象
        """
        obj = instance()

        if isinstance(data, dict):
            for key, val in data.items():
                setattr(obj, key, val)

        return obj

#
# class Node:
#     """
#     hash表的node节点
#     """
#
#     def __init__(self, name, value=None):
#         self.name = name
#         self.value = []
#         self.length = len(self.value)
#         if value is not None:
#             self.value.append(value)
#         self.updateLength()
#
#     def updateLength(self):
#         self.length = len(self.value)
#
#     def get(self):
#         """
#         获取节点下的最后一个值
#         """
#         return self.value[self.length - 1]
#
#     def clear(self):
#         """
#         清空node节点所有值
#         """
#         self.value.clear()
#
#
# class HashTable:
#     """
#     哈希表
#     """
#
#     def __init__(self, name=None, value=None):
#         self.nodes = []
#         if name is not None:
#             self.put(name, value)
#
#     def put(self, name, value):
#         """
#         添加一个节点
#         """
#         hashKey = hash(name)
#         node = Node(hashKey, value)
#         self.nodes.append(node)
#         self.reSorted()
#
#     def reSorted(self):
#         for i in range(len(self.nodes)):
#             for j in range(i, len(self.nodes) - 1):
#                 if self.nodes[i].name < self.nodes[j].name:
#                     temp = self.nodes[i]
#                     self.nodes[i] = self.nodes[j]
#                     self.nodes[j] = temp
#
#     def hasHash(self, name):
#         pass
#
#
# if __name__ == '__main__':
#     hashTable = HashTable()
#     hashTable.put('a', 'b')
#     hashTable.put('b', 'b')
#     hashTable.put('c', 'b')
#     hashTable.put('d', 'b')
