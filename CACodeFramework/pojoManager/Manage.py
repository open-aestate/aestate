from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.pojoManager import tag
from CACodeFramework.util import JsonUtil
from CACodeFramework.MainWork import CACodeRepository


class Pojo(CACodeRepository.Repository):
    def __init__(self, config_obj=None, log_conf=None, close_log=False, **kwargs):
        """
        初始化ORM框架
        """

        if '__table_name__' not in self.__dict__:
            self.__table_name__ = self.__class__.__name__

        if '__table_msg__' not in self.__dict__:
            self.__table_msg__ = 'The current object has no description'

        self.__table_name__ = self.__table_name__
        self.__table_msg__ = self.__table_msg__
        self.init_fields()
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        super(Pojo, self).__init__(config_obj=config_obj,
                                   participants=self,
                                   log_conf=log_conf,
                                   close_log=close_log)

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

    @staticmethod
    def is_default(val):
        """
        是否等于默认值
        """
        try:
            t_v = val.__class__.__bases__
            t_bf = tag.baseTag
            return t_v[len(t_v) - 1] == t_bf
        except SyntaxError:
            return False

    @property
    def orm(self):
        """
        转ORM框架
        """
        return CACodePureORM(self)

    def format(self, key, name):
        if 'ig' in self.__fields__.keys():
            self.__fields__['ig'].append({
                key: name
            })
        else:
            self.__fields__['ig'] = []
            self.format(key, name)
