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
