class Target:
    def __init__(self, text, node, parent):
        self._text = text
        self._node = node
        self._parent = parent
        self.SIZE = len(self._text)


class Tag:
    def __init__(self, root):
        self.root = root

    def parse(self) -> Target: ...

    def __str__(self):
        return str(self.root)

    def pure_str(self) -> str: ...


"""
===========================
顶层一级标签开始
============================
"""


class Namespace(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Database(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Template(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Description(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Include(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


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
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Elif(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Else(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Switch(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Case(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Default(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
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
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Select(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        texts = ["SELECT"]
        for i, v in enumerate(self.root.childNodes):
            if v.nodeName in XML_KEY.keys():
                obj = XML_KEY[v.nodeName](v)
                texts.add(node=obj.root, index=i)
            elif v.nodeName == XML_TEXT_NODE:
                texts.add(node=v, index=i)
        return texts


class Insert(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Update(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class Delete(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass


class From(Tag):
    def parse(self) -> Target:
        pass

    def pure_str(self) -> str:
        pass
