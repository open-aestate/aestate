__all__ = [
    'mat', 'CACode_SqlError', 'CACode_Factory_Error',
    'Json_Error', 'Syntax_Error', 'Attribute_Error',
    'Attribute_Error', 'Log_Opera_Name', 'Miss_Attr',
    'Error', 'Warn', 'Info',
    'Database_Operation', 'Parse_Error', 'FieldNotExist',
    'ModuleCreateError'
]


def mat(prefix, suffix):
    return '%s:%s' % (prefix, suffix)


def CACode_SqlError(msg):
    return mat('CACode-SqlError', msg)


def CACode_Factory_Error(msg):
    return mat('CACode-Factory', msg)


def Json_Error(msg):
    return mat('CACode-Json', msg)


def Syntax_Error(msg):
    return mat('CACode-SyntaxError', msg)


def Attribute_Error(msg):
    return mat('CACode-AttributeError', msg)


def Log_Opera_Name(msg):
    return mat('CACode-DatabaseOperation', msg)


def Miss_Attr(msg):
    return mat('CACode-Attribute', msg)


def Error():
    return 'ERROR'


def Warn():
    return 'WARNING'


def Info():
    return 'INFO'


def Database_Operation():
    return 'DATABASE OPERATION'


def Parse_Error(msg):
    return mat('CACode-Parse', msg)
