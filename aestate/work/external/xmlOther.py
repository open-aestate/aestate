from aestate.work.external import XML_IGNORE_NODES, XML_TEXT_NODE, XML_KEY


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
    xml = AestateXml.read_file("/example/config\\test.xml")
    child_child = xml.children
    print(child_child['item'][0].text)
