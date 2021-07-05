# -*- utf-8 -*-
# @Time: 2021/7/6 1:07
# @Author: CACode
from aestate.work.items import Append


class Operation:
    def __init__(self):
        self.append = Append()


class BaseModel:
    """
    基本的模块，继承此类后重写
    """

    def __init__(self, table_name: str, fields: list, config_obj: object):
        """
        :param table_name:表名字
        :param fields:使用的字段
        :param config_obj:配置类
        """
        self.table_name = table_name
        self.fields = fields
        self.config_obj = config_obj

    @classmethod
    def opera(cls):
        return Operation()

    def get_fields(self):
        """
        获取可用字段
        """
        return self.fields

    @property
    def __conn(self):
        return self.__conn

    def get_conn(self):
        pass

    def get_meta(self):
        if hasattr(self, 'meta'):
            pass
