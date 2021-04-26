from CACodeFramework.pojoManager import Manage
from CACodeFramework.pojoManager.Manage import Pojo


class BaseData(Pojo):
    def __init__(self):
        self.id = Manage.tag.intField()
        super(BaseData, self).__init__()
