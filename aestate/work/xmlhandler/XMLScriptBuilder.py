# -*- utf-8 -*-
from abc import ABC
from xml.dom.minidom import Element

from aestate.exception import TagHandlerError


class NodeHandler(ABC):
    """节点事件抽象"""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    # 操作
    def handleNode(self): ...


class IfHandler(NodeHandler):
    """if标签事件"""

    def handleNode(self):
        if self.initial_field != self.field:
            # 转换成同类型
            value = type(self.params[self.field])(self.value)
            if self.symbol == '>=':
                if self.params[self.field] >= value:
                    success = True
                else:
                    success = False
            elif self.symbol == '<=':
                if self.params[self.field] <= value:
                    success = True
                else:
                    success = False
            elif self.symbol == '==':
                if self.params[self.field] == value:
                    success = True
                else:
                    success = False
            elif self.symbol == '>':
                if self.params[self.field] > value:
                    success = True
                else:
                    success = False
            elif self.symbol == '<':
                if self.params[self.field] < value:
                    success = True
                else:
                    success = False
            else:
                raise TagHandlerError(
                    f'The node rule parsing failed and did not conform to the grammatical structure.{self.symbol}')
        else:
            if self.symbol == '>=':
                if self.field >= self.value:
                    success = True
                else:
                    success = False
            elif self.symbol == '<=':
                if self.field <= self.value:
                    success = True
                else:
                    success = False
            elif self.symbol == '==':
                if self.field == self.value:
                    success = True
                else:
                    success = False
            elif self.symbol == '>':
                if self.field > self.value:
                    success = True
                else:
                    success = False
            elif self.symbol == '<':
                if self.field < self.value:
                    success = True
                else:
                    success = False
            else:
                raise TagHandlerError(
                    f'The node rule parsing failed and did not conform to the grammatical structure.{self.symbol}')
        return success

    def checking_mark(self, node: Element):
        if node.nextSibling.nodeName == '#text':
            return self.checking_mark(node.nextSibling)
        else:
            if node.nextSibling.nodeName == 'else':
                return True
            else:
                return False
