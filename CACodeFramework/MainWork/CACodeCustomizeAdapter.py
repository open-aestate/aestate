from CACodeFramework.cacode.Serialize import QuerySet
from CACodeFramework.field.MySqlDefault import MySqlFields_Default


class Adapter(object):
    def __init__(self, repositoryId, serializer=QuerySet, sqlFields=MySqlFields_Default):
        self.repositoryId = repositoryId
        self.serializer = serializer

    def getFormId(self, obj_id):
        pass
