# -*- utf-8 -*-
import re
from abc import ABC
from xml.dom.minidom import Element

from aestate.exception import NotFindTemplateError, TagAttributeError, TagHandlerError
from aestate.work.xmlhandler.XMLScriptBuilder import IfHandler
from aestate.work.xmlhandler.base import AestateNode, TextNode


class AbstractNode(ABC):
    """抽象节点，所有节点的父类"""

    # 节点自身的操作

    def __init__(self, target_obj, params, aestate_xml_cls, root, value, XML_KEY, XML_IGNORE_NODES):
        self.target_obj = target_obj
        self.params = params
        self.aestate_xml_cls = aestate_xml_cls
        self.root = root
        self.node = value
        self.XML_KEY = XML_KEY
        self.XML_IGNORE_NODES = XML_IGNORE_NODES

    # 得到节点的值
    def apply(self, *args, **kwargs):
        ...

    def parseNode(self, texts: AestateNode, node: Element):
        for root_index, root_value in enumerate(node.childNodes):
            if root_value.nodeName in self.XML_KEY.keys():
                obj = self.XML_KEY[root_value.nodeName](self.target_obj, self.params, self.aestate_xml_cls, self.root,
                                                        root_value, self.XML_KEY, self.XML_IGNORE_NODES)
                texts = obj.apply(texts=texts)
            elif root_value.nodeName in self.XML_IGNORE_NODES:
                texts.add(node=root_value, index=root_index)
            texts.extend(AestateNode(self.root, root_value))
        return texts


class ImportNode(AbstractNode):
    """import标签"""

    def apply(self, *args, **kwargs):
        pass


class DatabaseNode(AbstractNode):
    """database标签"""

    def apply(self, *args, **kwargs):
        pass


class TemplateNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class ItemNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class SelectNode(AbstractNode):

    def apply(self, *args, **kwargs):
        # 取得已有的文本
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        # 返回值类型
        resultType = axc_node.attrs['resultType']
        texts.mark['resultType'] = resultType.text
        return self.parseNode(texts, self.node)


class InsertNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class UpdateNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class DeleteNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class IfNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        test_syntax = axc_node.attrs['test']
        syntax_re_text = re.findall('(.*?)([>=|<=|==|<|>]+)(.*)', test_syntax.text)
        if len(syntax_re_text) == 0:
            # 缺少必要的test标签语法
            raise TagAttributeError(f'The attribute`test` in the if tag is missing a required structure')
        # 移除空集
        syntax_using = [x for x in syntax_re_text[0] if x != '']
        if len(syntax_using) == 2 or len(syntax_using) > 3:
            raise TagHandlerError(
                f'The node rule parsing failed and did not conform to the grammatical structure.{syntax_using}')

        initial_field = syntax_using[0]
        symbol = syntax_using[1]
        value = syntax_using[2]

        rfield = re.findall('#{(.*?)}', initial_field)

        field = rfield[0] if len(rfield) > 0 and rfield[0] in self.params.keys() else initial_field
        # 让事件器来执行
        ih = IfHandler(initial_field=initial_field, field=field, params=self.params, value=value, symbol=symbol)

        success = ih.handleNode()

        if success:
            texts = self.parseNode(texts, node=self.node)

        if ih.checking_mark(self.node):
            # 设置为反的
            texts.mark['if_next'] = not success

        return texts


class ElseNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        if 'if_next' not in texts.mark.keys():
            raise TagHandlerError('Cannot find the if tag in front of the else tag')
        else:
            if_next = texts.mark['if_next']
            if not if_next:
                texts.mark.pop('if_next')
                return texts
            else:
                texts.mark.pop('if_next')
                return self.parseNode(texts, self.node)


class SwitchNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        field_name = axc_node.attrs['field'].text
        value = self.params[field_name]
        case_nodes = axc_node.children['case']
        check_node = None
        for cn in case_nodes:
            if cn.attrs['value'].text == value:
                check_node = cn.node
                break
        if check_node is None:
            check_node = axc_node.children['default'][0].node
        texts = self.parseNode(texts, check_node)

        return texts


class CaseNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class DefaultNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class IncludeNode(AbstractNode):

    def apply(self, *args, **kwargs):
        texts = kwargs['texts']
        axc_node = self.aestate_xml_cls(self.root, self.node, self.params)
        from_node_name = axc_node.attrs['from'].text
        templates = self.target_obj.xNode.children['template']
        target_template = None
        for t in templates:
            if t.attrs['id'].text == from_node_name:
                target_template = t
        if target_template is None:
            raise NotFindTemplateError(f'The template named `{from_node_name}` could not be found from the node')
        texts = self.parseNode(texts, target_template.node)
        return texts


class ResultMapNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class ResultNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass


class ForeignKeyNode(AbstractNode):

    def apply(self, *args, **kwargs):
        pass
