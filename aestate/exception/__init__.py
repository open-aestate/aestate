import traceback
from enum import Enum

from aestate.i18n import I18n


class DBException(Exception):
    def __init__(self, baseException):
        self.baseException = baseException
        self.baseName = self.baseException.__class__.__name__
        self.args = baseException.args
        super(DBException, self).__init__()

    def __str__(self):
        return f"({self.baseName}):{str(self.baseException)}"

    def println(self):
        traceback.print_exc(limit=1)


class ModuleCreateError(ModuleNotFoundError):
    """模块创建异常"""


class FieldNotExist(AttributeError):
    """字段不存在"""


class SqlSyntaxError(Exception):
    """sql语法"""


class SqlResultError(DBException):
    """sql返回错误"""


class XmlParseError(Exception):
    """xml解析错误"""


class NotFindTemplateError(XmlParseError):
    """找不到xml模板"""


class TagAttributeError(XmlParseError):
    """节点属性错误"""


class TagHandlerError(XmlParseError):
    """节点处理方式错误"""


class BaseSqlError:
    def __init__(self, exception):
        self.exception = exception
        self.text = str(exception)

    def raise_exception(self, **kwargs):
        self.exception.args = list(self.exception.args)
        # DBException(self.exception).println()
        raise DBException(self.exception)


class LogStatus(Enum):
    Error = 'ERROR'
    Warn = 'WARN'
    Info = 'INFO'


# 错误描述国际化
ExceptionMessage = I18n()
