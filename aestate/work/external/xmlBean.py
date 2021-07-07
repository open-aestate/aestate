from aestate.work.Manage import Pojo


class Target(str):
    pass


class Table(Pojo):
    """
    表
    """

    def __init__(self, db, name):
        self.db = db
        self.name = name

    def __str__(self):
        return self.name


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


class Select(Tag):
    def parse(self):
        pass
