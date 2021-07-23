from aestate.exception import FieldNotExist
from aestate.util.Log import CACodeLog

XML_TEXT_NODE = ['#text', 'description']


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
