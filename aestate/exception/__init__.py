import re


class DBException(Exception):
    def __init__(self, baseException):
        self.baseException = baseException
        self.baseName = self.baseException.__class__.__name__
        super(DBException, self).__init__()

    def __str__(self):
        return f"({self.baseName}):{str(self.baseException)}"


class ModuleCreateError(ModuleNotFoundError):
    pass


class FieldNotExist(AttributeError):
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
            self.err_text = "sql语句拼写错误,错误内容:(%s)" % err_content[0]
        return self.err_text


class MySqlErrorTest(BaseMySqlError):

    def ver(self):
        mer = MySqlErrorRegular(self.text)
        err_text = mer.syntax_error()
        self.text = err_text
        return err_text
