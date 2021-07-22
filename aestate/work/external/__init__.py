# xml忽略解析的节点，文本和注释
from aestate.work.external.xmlBean import *

XML_TEXT_NODE = '#text'
XML_COMMENT_NODE = '#comment'
XML_IGNORE_NODES = [XML_TEXT_NODE, XML_COMMENT_NODE]
XML_KEY = {
    'namespace': Namespace,
    'database': Database,
    'template': Template,
    'description': Description,
    'include': Include,
    'if': If,
    'elif': Elif,
    'else': Else,
    'switch': Switch,
    'case': Case,
    'default': Default,
    'where': Where,
    'select': Select,
    'insert': Insert,
    'update': Update,
    'delete': Delete,
    'from': From,
}
