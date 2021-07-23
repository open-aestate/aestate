from aestate.ajson import aj
from aestate.exception import FieldNotExist

from aestate.work.Serialize import QuerySet
from aestate.work.orm import CACodePureORM
from aestate.dbs._mysql import tag
from aestate.work import repository
from aestate.work import Banner


class Pojo(repository.Repository):
    def __init__(self, config_obj=None, log_conf=None, close_log=False, serializer=QuerySet, **kwargs):
        """
        初始化ORM框架
        :param config_obj:配置类
        :param log_conf:日志配置类
        :param close_log:是否关闭日志显示功能
        :param serializer:自定义序列化器,默认使用CACodeFramework.cacode.Serialize.QuerySet
        """
        # aestate logo
        Banner.show()

        if not hasattr(self, '__table_name__'):
            self.__table_name__ = self.__class__.__name__
        if not hasattr(self, '__table_msg__'):
            self.__table_msg__ = 'The current object has no description'

        self._fields = {}
        # 在这里将config_obj实例化
        self.serializer = serializer
        # 忽略的字段
        self.__ignore_field__ = {}
        # 添加的字段
        self.__append_field__ = {}
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        self.init_fields()
        super(Pojo, self).__init__(config_obj=config_obj,
                                   instance=self,
                                   log_conf=log_conf,
                                   close_log=close_log,
                                   serializer=serializer,
                                   **kwargs)

    def init_fields(self):
        """
        初始化字段
        """
        fields = self.__dict__
        fds = {}
        for key, value in fields.items():
            # 取出这个值引用对象的父类
            try:
                t_v = value.__class__.__base__
                if t_v in [tag.Template, tag.baseTag]:
                    if not hasattr(self, key) or getattr(self, key) is None or t_v in [tag.Template, tag.baseTag]:
                        setattr(self, key, value.default)
                    fds[key] = value
                    fds[key].name = key
            except SyntaxError:
                continue

        self._fields = fds

    def to_json(self, bf=False):
        """
        将此叶子节点转json处理
        """
        # 从内存地址获取限定对象
        # 将需要的和不需要的合并

        # 得到当前所有的字段
        all_fields = self.getFields()
        # 合并字段
        all_fields = dict(all_fields, **self.__append_field__)
        # 删除忽略字段
        for i in self.__ignore_field__.keys():
            if i in all_fields.keys():
                del all_fields[i]

        new_dict = {}
        for key in all_fields.keys():
            # 当字段为未填充状态时，默认定义为空
            new_dict[key] = getattr(self, key) if hasattr(self, key) else all_fields[
                key] if key in all_fields.keys() else None
        return aj.parse(new_dict, bf=bf)

    def to_dict(self):
        """
        将数据集转字典格式
        """
        return aj.load(self.to_json())

    def getFields(self) -> dict:
        """
        获取当前类所需要序列化的字段
        """
        return self._fields

    def add_field(self, key, default_value=None):
        """
        添加一个不会被解析忽略的字段
        """
        if key not in self.__append_field__.keys():
            self.__append_field__[key] = default_value

    def remove_field(self, key):
        """
        添加一个会被解析忽略的字段
        """
        self.__ignore_field__[key] = None

    @property
    def orm(self):
        """
        转ORM框架
        """
        return CACodePureORM(repository=self)

    def format(self, key, name):
        """
        为指定字段的值设置别名
        """
        if 'ig' in self.getFields().keys():
            self._fields['ig'].append({
                key: name
            })
        else:
            self._fields['ig'] = []
            self.format(key, name)

    def __str__(self):
        """
        """
        return self.__table_name__

    def get_tb_name(self):
        """
        获取当前pojo的表名
        """
        return self.__table_name__

    def get_database(self):
        """
        获取当前pojo的数据库连接对象
        """
        if hasattr(self, 'config_obj'):
            return self.config_obj
        raise FieldNotExist("pojo对象暂未初始化，没有获取到配置项")
