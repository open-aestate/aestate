# -*- utf-8 -*-
# @Time: 2021/7/6 0:58
# @Author: CACode
from _typeshed import SupportsLessThanT
from typing import List


class BaseItems:
    def __init__(self, expression):
        self._text = expression

    def __str__(self):
        return self._text


class Column:
    """
    列
    """


class Function:
    """
    方法
    """


class Append(list):
    """
    追加
    """

    def __init__(self, expression: object):
        """
        :param expression:表达式
        """
        list.__init__([])
        self.expression = expression

    @staticmethod
    def exp_init(cls):
        return cls.__new__(expression=None)

    def sort(self: List[SupportsLessThanT], *, key: None = ..., reverse: bool = ...) -> None:
        pass
