from aestate.work.Manage import Pojo


class Target:
    def __init__(self, text, node, parent):
        self._text = text
        self._node = node
        self._parent = parent
        self.SIZE = len(self._text)


class Table:
    """
    表
    """

    def __init__(self, target_pojo):
        self.pojo = target_pojo

    @property
    def name(self) -> str:
        return self.pojo.get_tb_name()

    @property
    def db_name(self) -> str:
        return self.pojo.get_database()

    def __str__(self):
        return "{}.{}".format(self.db_name, self.name)


class Tag:
    def __init__(self, source_text, this: Table, children: list):
        """
        :param source_text:当前标记下的源文本，不包含子标签
        :param this:当前的操作归属的表
        :param children:当前标记下的子节点
        """
        self._source_text = source_text
        self._children = children
        self._this = this

    def parse(self) -> Target: ...

    def __str__(self):
        return str(self._this) + '.' + self._source_text

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
        pass


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
