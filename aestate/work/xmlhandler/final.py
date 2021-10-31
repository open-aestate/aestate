# -*- utf-8 -*-
from aestate.work.xmlhandler.nodes import SelectNode, \
    UpdateNode, IfNode, ElseNode, SwitchNode, IncludeNode

XML_IGNORE_NODES = ['#text']
XML_KEY = {
    'select': SelectNode,
    'update': UpdateNode,
    'if': IfNode,
    'else': ElseNode,
    'switch': SwitchNode,
    'include': IncludeNode,
}
