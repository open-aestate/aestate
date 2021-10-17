# -*- utf-8 -*-
from aestate.exception import FieldNotExist
from aestate.util.Log import CACodeLog


class Target:
    def __init__(self, text, node, parent):
        self._text = text
        self._node = node
        self._parent = parent
        self.SIZE = len(self._text)

    @property
    def text(self):
        return self._text


class Tag:
    def __init__(self, model, root, node, temps: dict):
        self.model = model
        self.root = model(root, root)
        self.node = model(root, node)
        self.temps = temps

    def __str__(self):
        return str(self.root)

    def pure_str(self) -> Target: ...


"""
===========================
顶层一级标签开始
============================
"""


class Namespace(Tag):

    def pure_str(self) -> Target:
        pass


class Database(Tag):

    def pure_str(self) -> Target:
        pass


class Template(Tag):

    def pure_str(self) -> Target:
        pass


class Description(Tag):

    def pure_str(self) -> Target:
        pass


class Include(Tag):

    def pure_str(self) -> Target:
        template_node = None
        for temp in self.root.children['template']:
            if 'id' in temp.attrs.keys() and temp.attrs['id'].text == self.node.attrs['from'].text:
                template_node = temp
                break

        if not template_node:
            CACodeLog.log_error(msg=f"The template tag with id `{self.node.attrs['from'].text}` was not found",
                                obj=FieldNotExist,
                                raise_exception=True)

        return template_node.text


"""
===========================
顶层一级标签结束
============================
"""

"""
===========================
具有逻辑型的标签开始
============================
"""


class If(Tag):

    def pure_str(self) -> Target:
        pass


class Elif(Tag):

    def pure_str(self) -> Target:
        pass


class Else(Tag):

    def pure_str(self) -> Target:
        pass


class Switch(Tag):

    def pure_str(self) -> Target:
        pass


class Case(Tag):

    def pure_str(self) -> Target:
        pass


class Default(Tag):

    def pure_str(self) -> Target:
        pass


"""
===========================
具有逻辑型的标签结束
============================
"""

"""
===========================
sql基本方言标签开始
============================
"""


class Where(Tag):

    def pure_str(self) -> Target:
        pass


class Select(Tag):
    def pure_str(self) -> Target:
        texts = ['SELECT']
        for root_index, root_value in self.node.children.items():
            t = []
            for child_index, child_value in enumerate(root_value):
                if child_value.node.nodeName in self.temps.keys():
                    obj = self.temps[child_value.node.nodeName](self.model, self.root, child_value, self.temps)
                    texts.append(obj.pure_str())
                elif child_value.node.nodeName in XML_TEXT_NODE:
                    texts.append(child_value.text)
            texts.extend(t)
        return Target(' '.join(texts), self.node, self.root)


class Insert(Tag):

    def pure_str(self) -> Target:
        pass


class Update(Tag):

    def pure_str(self) -> Target:
        pass


class Delete(Tag):

    def pure_str(self) -> Target:
        pass


class From(Tag):

    def pure_str(self) -> Target:
        pass


XML_TEXT_NODE = ['#text', 'description']
XML_IGNORE_NODES = ['description']
XML_KEY = {
    'namespace': Namespace,
    'database': Database,
    'template': Template,
    'description': Description,
    'include': Include,
    'if': If,
    'elif': Elif,
    'else': Else,
    'switch': Switch,
    'case': Case,
    'default': Default,
    'where': Where,
    'select': Select,
    'insert': Insert,
    'update': Update,
    'delete': Delete,
    'from': From,
}


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


class AestateTextNode(list):
    def __init__(self, root, node):
        list.__init__([])
        self.root = root
        self.node = node

    def add(self, node, index) -> None:
        self.append(TextNode(self.root, node, index))

    @property
    def text(self):
        arr = sorted(self, key=lambda x: x.index)
        texts = [i.text for i in arr]
        # for i, v in enumerate(arr):
        #     if v.node.nodeName in XML_KEY.keys():
        #         obj = XML_KEY[v.node.nodeName](v)
        #         texts.append(obj.pure_str(XML_KEY))
        #     elif v.node.nodeName in XML_TEXT_NODE:
        #         texts.append(v.node.data)
        return ' '.join(texts)

    def __str__(self) -> str:
        return self.text


def parse_children(root, elements):
    """
    获取所有子节点
    """
    child_list = {}
    for i in elements:
        node_name = i.nodeName if hasattr(i, 'nodeName') else i.node.nodeName
        if node_name not in XML_IGNORE_NODES:
            if node_name not in child_list.keys():
                child_list[node_name] = []
            child_list[node_name].append(AestateXml(root=root, node=i))
    return child_list


def parse_attributes(attr):
    if attr is None:
        return {}
    objs = {}
    for k, v in attr._attrs.items():
        objs[k] = Attribute(name=k, node=v)
    return objs


class AestateXml:
    """
    xml对象
    """

    def __init__(self, root, node):
        self.root = root
        self.node = node
        self.children = parse_children(node, node.childNodes if hasattr(node, 'childNodes') else node.children)
        self.tags = {}
        self.attrs = parse_attributes(node.attributes if hasattr(node, 'attributes') else node.attrs)

    @property
    def text(self):
        texts = AestateTextNode(self.root, self.node)
        for root_index, root_value in enumerate(self.node.childNodes):
            t = AestateTextNode(self.root, root_value)
            if root_value.nodeName in XML_KEY.keys():
                obj = XML_KEY[root_value.nodeName](AestateXml, self.root, root_value, XML_KEY)
                texts.add(node=obj.pure_str(), index=root_index)
            elif root_value.nodeName in XML_TEXT_NODE:
                texts.add(node=root_value, index=root_index)

            texts.extend(t)
        return texts.text

    def open_stack(self):
        """
        开拓内存空间，并固定位置为
        """
        pass

    @staticmethod
    def read_file(filename):
        """
        读取xml文件
        """
        from xml.dom import minidom
        build = minidom.parse(filename)
        root = build.documentElement
        return AestateXml(root=root, node=root)


if __name__ == '__main__':
    xml = AestateXml.read_file("G:\\Github\\AestateFramework\\example\\tables\\test.xml")
    child_child = xml.children
    print(child_child['item'][0].text)
