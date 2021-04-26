JSON_ERROR = 'CACode-Json'
SYNTAX_ERROR = 'CACode-Syntax'
ATTR_ERROR = 'CACode-Attr'
LOG_OPERA_NAME = 'CACode-Database-Operation'
WARN = 'WARN'
INFO = 'INFO'
DB_TASK = 'DATABASE OPERATION'
PARSE_ERROR = 'CACode-Parse'


# INSTANCES_ERROR = 'CACode-Factory'


def CACode_SQLERROR(msg):
    return '%s:%s' % ('CACode-Sql', msg)


def CACode_Factory_Error(msg):
    return 'CACode-Factory:{}'.format(msg)
