import re


class DBException(Exception):
    def __init__(self, baseException):
        self.baseException = baseException
        self.baseName = self.baseException.__class__.__name__
        super(DBException, self).__init__()

    def __str__(self):
        return f"({self.baseName}):{str(self.baseException)}"


class ModuleCreateError(ModuleNotFoundError):
    """模块创建异常"""


class FieldNotExist(AttributeError):
    """字段不存在"""


class SqlResultError(DBException):
    pass


class XmlParseError(Exception):
    pass


class NotFindTemplateError(XmlParseError):
    pass


class TagAttributeError(XmlParseError):
    pass


class TagHandlerError(XmlParseError):
    pass


class BaseMySqlError:
    def __init__(self, exception):
        self.exception = exception
        self.text = str(exception)

    def ver(self):
        return self.text

    def raise_exception(self):
        ar = self.exception.args
        ar_array = list(ar)
        ar_array[len(ar_array) - 1] = self.text
        self.exception.args = ar_array
        raise DBException(self.exception)


class MySqlErrorRegular:
    def __init__(self, text):
        self.text = text
        self.err_text = text

    def syntax_error(self):
        flag = re.compile("You have an error in your SQL syntax[\w\W].*use near([\w\W].*)")
        err_content = flag.findall(self.text)
        if err_content:
            self.err_text = "sql statement spelling error, wrong content:(%s)" % err_content[0]
        return self.err_text

    def format_err(self):
        flag = re.compile(".*not all arguments converted during string formatting.*")
        err_content = flag.findall(self.text)
        if err_content:
            self.err_text = "The parameter does not correspond to the number of formatted strings:(%s)" % err_content[0]
        return self.err_text


class MySqlErrorTest(BaseMySqlError):

    def ver(self):
        mer = MySqlErrorRegular(self.text)
        mer.syntax_error()
        mer.format_err()
        self.text = mer.err_text
        return self.text
