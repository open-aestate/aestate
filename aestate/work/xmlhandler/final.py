# -*- utf-8 -*-
from aestate.work.xmlhandler.sqlNode import ImportNode, DatabaseNode, TemplateNode, ItemNode, SelectNode, \
    InsertNode, UpdateNode, DeleteNode, IfNode, ElseNode, SwitchNode, CaseNode, DefaultNode, IncludeNode, \
    ResultMapNode, ResultNode, ForeignKeyNode

XML_IGNORE_NODES = ['#text']
XML_KEY = {
    'import': ImportNode,
    'database': DatabaseNode,
    'template': TemplateNode,
    'item': ItemNode,
    'select': SelectNode,
    'insert': InsertNode,
    'update': UpdateNode,
    'delete': DeleteNode,
    'if': IfNode,
    'else': ElseNode,
    'switch': SwitchNode,
    'case': CaseNode,
    'default': DefaultNode,
    'include': IncludeNode,
    'resultMap': ResultMapNode,
    'result': ResultNode,
    'foreignKey': ForeignKeyNode
}
