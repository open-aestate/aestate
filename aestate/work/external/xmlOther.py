from aestate.work.external import XML_IGNORE_NODES, XML_TEXT_NODE


class TextNode:
    def __init__(self, node, index):
        self.node = node
        self.index = index

    def __str__(self):
        return self.node.data


class AestateTextNode(list):
    def __init__(self):
        list.__init__([])
        self.textNode = []

    def append(self, node, index) -> None:
        self.textNode.append(TextNode(node, index))

    def __str__(self) -> str:
        return ''.join([str(i) for i in self.textNode])


class AestateXml:
    """
    xml对象
    """

    def __init__(self, root, children):
        self.root = root
        self.children = self.parse_children(children)
        self.tags = {}

    def parse_children(self, elements):
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

    @property
    def text(self):
        texts = AestateTextNode()
        for i, v in enumerate(self.root.childNodes):
            if v.nodeName == XML_TEXT_NODE:
                texts.append(node=v, index=i)
        return texts

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
    xml = AestateXml.read_file("D:\\gitProjects\\aestate-xml\\v1\\test_tags.xml")
    child_child = xml.children
    print(xml.text)
