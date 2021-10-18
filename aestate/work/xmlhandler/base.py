# -*- utf-8 -*-
from _ast import AST


class Attribute:
    def __init__(self, name, node):
        self.root = node
        self.text = node.value
        self.name = name


class TextNode:
    def __init__(self, root, node, index):
        self.root = root
        self.node = node
        self.index = index
        self.childNodes = node.childNodes if hasattr(node, 'childNodes') else None
        self.attributes = node.attributes if hasattr(node, 'attributes') else None

    @property
    def text(self):
        return self.node.text if hasattr(self.node, 'text') else self.node.data

    def __str__(self):
        return self.node.text


class AestateNode(list):
    def __init__(self, root, node):
        list.__init__([])
        self.root = root
        self.node = node
        # 给定一个标记，让剩下的标签允许存放信息
        self.mark = {}

    def add(self, node, index) -> None:
        self.append(TextNode(self.root, node, index))

    @property
    def text(self):
        texts = [i.text for i in self]
        # for i, v in enumerate(arr):
        #     if v.node.nodeName in XML_KEY.keys():
        #         obj = XML_KEY[v.node.nodeName](v)
        #         texts.append(obj.pure_str(XML_KEY))
        #     elif v.node.nodeName in XML_TEXT_NODE:
        #         texts.append(v.node.data)
        return ' '.join(texts)

    def __str__(self) -> str:
        return self.text


def parse_attributes(attr):
    if attr is None:
        return {}
    objs = {}
    for k, v in attr._attrs.items():
        objs[k] = Attribute(name=k, node=v)
    return objs


class ResultAST(AST):
    """返回值的ast抽象语法树"""

    @staticmethod
    def parse(resultMap):
        pass
