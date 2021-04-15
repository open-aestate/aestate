from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.field import field_tag
from CACodeFramework.util import JsonUtil
from CACodeFramework.MainWork import CACodeRepository


class POJO(CACodeRepository.Repository):
    def __init__(self, config_obj=None, log_conf=None, close_log=False, **kwargs):
        """
        初始化ORM框架
        """
        self.__table_name__ = self.__table_name__
        self.__table_msg__ = self.__table_msg__
        self.fields = self.init_fields()
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        super(POJO, self).__init__(config_obj=config_obj,
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
                t_bf = field_tag.baseTag
                if t_v[0] == t_bf:
                    fds[key] = value
            except SyntaxError:
                continue
        return fds

    def to_json(self):
        """
        将此对象转换为json

        无视时间报错
        """
        return JsonUtil.parse(self)

    def to_dict(self):
        """
        将此对象转换成字典格式
        """
        return self.fields

    def eq_default(self, val):
        """
        是否等于默认值
        """
        try:
            t_v = val.__class__.__bases__
            t_bf = field_tag.baseTag
            return t_v[0] == t_bf
        except SyntaxError:
            return False

    @property
    def orm(self):
        """
        转ORM框架
        """
        return CACodePureORM(self)


class tinyintField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(tinyintField, self).__init__(**kwargs)


class intField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(intField, self).__init__(**kwargs)


class bigintField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(bigintField, self).__init__(**kwargs)


class floatField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(floatField, self).__init__(**kwargs)


class doubleField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(doubleField, self).__init__(**kwargs)


class datetimeField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(datetimeField, self).__init__(**kwargs)


class charField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(charField, self).__init__(**kwargs)


class varcharField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(varcharField, self).__init__(**kwargs)


class textField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(textField, self).__init__(**kwargs)


class tinytextField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(tinytextField, self).__init__(**kwargs)


class longtextField(field_tag.baseTag):
    def __init__(self, **kwargs):
        super(longtextField, self).__init__(**kwargs)
