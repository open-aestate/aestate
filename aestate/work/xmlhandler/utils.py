# -*- utf-8 -*-
from aestate.work.xmlhandler.base import AestateNode, parse_attributes
from aestate.work.xmlhandler.final import XML_KEY, XML_IGNORE_NODES


def parse_children(root, elements, params):
    """
    获取所有子节点
    """
    child_list = {}
    for i in elements:
        node_name = i.nodeName if hasattr(i, 'nodeName') else i.node.nodeName
        if node_name not in XML_IGNORE_NODES:
            if node_name not in child_list.keys():
                child_list[node_name] = []
            child_list[node_name].append(AestateXml(root=root, node=i, params=params))
    return child_list


class AestateXml:
    """
    xml对象
    """

    def __init__(self, root, node, params: None):
        self.root = root
        self.node = node
        self.params = params if params else {}
        self.children = parse_children(node, node.childNodes if hasattr(node, 'childNodes') else node.children, params)
        self.tags = {}
        self.attrs = parse_attributes(node.attributes if hasattr(node, 'attributes') else node.attrs)
        self.resultType = None

    def text(self, target_obj):

        texts = AestateNode(self.root, self.node)
        for root_index, root_value in enumerate(self.node.childNodes):
            t = AestateNode(self.root, root_value)
            if root_value.nodeName in XML_KEY.keys():
                obj = XML_KEY[root_value.nodeName](target_obj, self.params, AestateXml, self.root, root_value, XML_KEY,
                                                   XML_IGNORE_NODES)
                texts = obj.apply(texts=texts)
            elif root_value.nodeName in XML_IGNORE_NODES:
                texts.add(node=root_value, index=root_index)
            texts.extend(t)
        return texts

    @staticmethod
    def read_file(filename):
        """
        读取xml文件
        """
        from xml.dom import minidom
        build = minidom.parse(filename)
        root = build.documentElement
        return AestateXml(root=root, node=root, params=None)
