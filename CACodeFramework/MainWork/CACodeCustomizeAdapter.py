from CACodeFramework.cacode.Serialize import QuerySet
from CACodeFramework.field.MySqlDefault import MySqlFields_Default


class Adapter(object):
    """
    适配器,将sql方言适配到ORM框架中,实现sql自由


    从配置表中开始配置sql方言,继承SqlLanguage类并实现抽象方法,开启



    """

    def __init__(self, repositoryId, serializer=QuerySet, sqlFields=MySqlFields_Default):
        self.repositoryId = repositoryId
        self.serializer = serializer
        self.sqlFields = sqlFields()
        self.sql = []

    def getFormId(self, obj_id):
        pass

    def setField(self, string):
        """
        设置一个字段
        """
        self.sql.append("{}{}{}".format(self.sqlFields.space, string, self.sqlFields.space))
