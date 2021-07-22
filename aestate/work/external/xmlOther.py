from aestate.work.external import XML_IGNORE_NODES, XML_TEXT_NODE, XML_KEY


class Attribute:
    def __init__(self, name, node):
        self.root = node
        self.text = node.value
        self.name = name


class TextNode:
    def __init__(self, node, index):
        self.node = node
        self.index = index

    def __str__(self):
        return self.node.data


class AestateTextNode(list):
    def __init__(self):
        list.__init__([])

    def add(self, node, index) -> None:
        self.append(TextNode(node, index))

    @property
    def text(self):
        arr = sorted(self, key=lambda x: x.index)
        texts = []
        for i, v in enumerate(arr):
            if v.node.nodeName in XML_KEY.keys():
                obj = XML_KEY[v.node.nodeName](v)
                texts.append(obj.pure_str())
            elif v.node.nodeName == XML_TEXT_NODE:
                texts.append(v.node.data)
        return ' '.join(texts)

    def __str__(self) -> str:
        return self.text


def parse_children(elements):
    """
    获取所有子节点
    """
    child_list = {}
    for i in elements:
        if i.nodeName not in XML_IGNORE_NODES:
            if i.nodeName not in child_list.keys():
                child_list[i.nodeName] = []
            child_list[i.nodeName].append(AestateXml(root=i, children=i.childNodes))
    return child_list


def parse_attributes(attr):
    objs = {}
    for k, v in attr._attrs.items():
        objs[k] = Attribute(name=k, node=v)
    return objs


class AestateXml:
    """
    xml对象
    """

    def __init__(self, root, children):
        self.root = root
        self.children = parse_children(children)
        self.tags = {}
        self.attrs = parse_attributes(root.attributes)

    @property
    def text(self):
        texts = AestateTextNode()
        for i, v in enumerate(self.root.childNodes):
            t = AestateTextNode()
            for i, v in enumerate(v.childNodes):
                if v.nodeName in XML_KEY.keys():
                    obj = XML_KEY[v.nodeName](v)
                    texts.add(node=obj.root, index=i)
                elif v.nodeName == XML_TEXT_NODE:
                    texts.add(node=v, index=i)

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
        return AestateXml(root=root, children=root.childNodes)


if __name__ == '__main__':
    xml = AestateXml.read_file("G:\\Github\\AestateFramework\\example\\tables\\test.xml")
    child_child = xml.children
    print(child_child['item'][0].text)
