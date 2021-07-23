# xml忽略解析的节点，文本和注释
from aestate.work.external.xmlBean import Namespace, Database, Template, Description, Include, If, Elif, \
    Else, Switch, Case, Default, Where, Select, Insert, Update, Delete, From

XML_TEXT_NODE = ['#text']
XML_IGNORE_NODES = ['description']
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
