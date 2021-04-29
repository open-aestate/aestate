from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.cacode.Serialize import QuerySet
from CACodeFramework.pojoManager import tag
from CACodeFramework.cacode.Serialize import JsonUtil
from CACodeFramework.MainWork import CACodeRepository


class Pojo(CACodeRepository.Repository):
    def __init__(self, config_obj=None, log_conf=None, close_log=False, serializer=QuerySet, **kwargs):
        """
        初始化ORM框架
        :param config_obj:配置类
        :param log_conf:日志配置类
        :param close_log:是否关闭日志显示功能
        :param serializer:自定义序列化器,默认使用CACodeFramework.cacode.Serialize.QuerySet
        """

        if not hasattr(self, '__table_name__'):
            self.__table_name__ = self.__class__.__name__

        if not hasattr(self, '__table_msg__'):
            self.__table_msg__ = 'The current object has no description'

        self.__table_name__ = self.__table_name__
        self.__table_msg__ = self.__table_msg__
        self.init_fields()
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        # 在这里将config_obj实例化
        self.serializer = serializer
        super(Pojo, self).__init__(config_obj=config_obj,
                                   participants=self,
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
                t_v = value.__class__.__bases__
                t_bf = tag.baseTag
                if t_v[0] == t_bf:
                    fds[key] = value
            except SyntaxError:
                continue

        self.fields = fds
        self.__fields__ = fds

    def to_json(self, bf=False):
        """
        将此对象转换为json

        :param bf:是否需要格式化

        无视时间报错
        """
        return JsonUtil.parse(self, bf)

    def to_dict(self):
        """
        将此对象转换成字典格式
        """
        return JsonUtil.load(JsonUtil.parse(self))

    @property
    def orm(self):
        """
        转ORM框架
        """
        return CACodePureORM(self, self.serializer)

    def format(self, key, name):
        """
        为指定字段的值设置别名
        """
        if 'ig' in self.__fields__.keys():
            self.__fields__['ig'].append({
                key: name
            })
        else:
            self.__fields__['ig'] = []
            self.format(key, name)
