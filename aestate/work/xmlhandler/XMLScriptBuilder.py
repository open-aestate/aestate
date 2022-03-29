# -*- utf-8 -*-
from abc import ABC
from xml.dom.minidom import Element

from aestate.exception import TagHandlerError
from aestate.util.Log import ALog


class NodeHandler(ABC):
    """节点事件抽象"""

    # 操作
    def handleNode(self, target_obj): ...


class IfHandler(NodeHandler):
    """if标签事件"""

    def __init__(self, initial_field, field, params, value, symbol):
        self.initial_field = initial_field
        self.field = field
        self.params = params
        self.value = value
        self.symbol = symbol

    def parse_node(self):
        pass

    def handleNode(self, target_obj):
        if self.initial_field != self.field:
            # 转换成同类型
            value = type(self.params[self.field])(self.value)
            if self.symbol == '>=':
                success = self.params[self.field] >= value
            elif self.symbol == '<=':
                success = self.params[self.field] <= value
            elif self.symbol == '==':
                success = self.params[self.field] == value
            elif self.symbol == '!=':
                success = self.params[self.field] != value
            elif self.symbol == '>':
                success = self.params[self.field] > value
            elif self.symbol == '<':
                success = self.params[self.field] < value
            else:
                ALog.log_error(
                    msg=f'The node rule parsing failed and did not conform to the grammatical structure.{self.symbol}',
                    obj=TagHandlerError, LogObject=target_obj.log_obj, raise_exception=True)
                success = False
        else:
            # UPDATE 1.0.6a2 如果匹配不到key就设置为None
            if self.symbol != '!=':
                ALog.log_error(
                    msg=f'`None` cannot judge `value`.wrong compiled field:`{self.field}{self.symbol}{self.value}`',
                    obj=TagHandlerError, LogObject=target_obj.log_obj, raise_exception=True)
                success = False
            else:
                #
                success = self.value == 'None' \
                          or self.value == 'false' \
                          or self.value == 'False' \
                          or self.value == '' \
                          or self.value == 0
            # if self.symbol == '>=':
            #     success = self.field >= self.value
            # elif self.symbol == '<=':
            #     success = self.field <= self.value
            # elif self.symbol == '==':
            #     success = self.field == self.value
            # elif self.symbol == '!=':
            #     success = self.field != self.value
            # elif self.symbol == '>':
            #     success = self.field > self.value
            # elif self.symbol == '<':
            #     success = self.field < self.value
            # else:
            #     ALog.log_error(
            #         msg=f'The node rule parsing failed and did not conform to the grammatical structure.{self.symbol}',
            #         obj=TagHandlerError, LogObject=target_obj.log_obj, raise_exception=True)
            #     success = False
        return success

    @staticmethod
    def checking_mark(node: Element):
        if node.nextSibling:
            if node.nextSibling.nodeName == '#text':
                return IfHandler.checking_mark(node.nextSibling)
            else:
                if node.nextSibling.nodeName == 'else':
                    return True
                else:
                    return False
        return False
