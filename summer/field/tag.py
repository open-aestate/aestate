import datetime

from summer.cacode.Serialize import JsonUtil

"""
这个文件用来为pojo对象做标记，当对象为空或为以下任意类型时
insert操做将会忽略该字段，find操作不会处理为空的字段
"""


class baseTag(object):
    def __init__(self,
                 name=None,
                 length=None,
                 d_point=None,
                 t_type='varchar',
                 is_null=False,
                 primary_key=False,
                 comment="",
                 auto_field=False,
                 auto_time=False,
                 update_auto_time=False,
                 default=None):
        """
        :param name:字段名
        :param length:长度
        :param d_point:小数点
        :param t_type:类型
        :param is_null:允许为空
        :param primary_key:键
        :param comment:注释
        :param auto_field:自增长键
        :param auto_time:默认设置当前时间
        :param update_auto_time:默认设置当前时间并根据当前时间更新
        :param default:默认值
        """
        # 是否为随着时间而更新
        self.update_auto_time = update_auto_time
        if update_auto_time:
            self.default = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 是否自动设置为当前时间
        self.auto_time = auto_time
        if auto_time:
            self.default = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 是否为自增
        self.autoField = auto_field
        # 注释
        self.comment = comment
        # 是否为主键
        self.primary_key = primary_key
        # 是否可以为空
        self.is_null = is_null
        # 小数点包含的位数
        self.d_point = d_point
        # 字段的名称
        self.name = name
        # 类型
        self.t_type = t_type
        # 最大长度
        self.length = length
        # 如果有设置自定义默认值则用自定义,如果有其他的条件触发默认值则设置,反之为空
        self.default = default if default else self.default if hasattr(self, 'default') else None
        # 如果使用的是被继承的子类，那么在这里就会有一个名为fields的字段
        # 将所有自定义字段
        if self.fields:
            for key, value in self.fields.items():
                setattr(self, key, value)

            del self.fields

    def get_field(self, name):
        """
        获得字段
        """
        return getattr(self, name)

    def set_field(self, name, value):
        """
        设置值
        """
        setattr(self, name, value)

    def get_table(self, bf):
        """
        获取表数据结构
        """
        if bf:
            return JsonUtil.parse(self, bf)
        return JsonUtil.load(JsonUtil.parse(self))


class Template(baseTag):

    def __init__(self, cls=None, **kwargs):
        self.fields = {}
        self.t_type = self.t_type
        if cls:
            kwargs.update(cls.__dict__)
            self.fields['cls'] = cls
        kwargs.update(update_field(**kwargs))
        self.fields.update(kwargs)
        super(Template, self).__init__(**kwargs)


class tinyintField(Template):
    """
    CREATE TABLE IF NOT EXISTS `runoob_tbl`(
           `runoob_id` INT UNSIGNED AUTO_INCREMENT,
           `runoob_title` VARCHAR(100) NOT NULL,
           `runoob_author` VARCHAR(40) NOT NULL,
           `submission_date` DATE,
           PRIMARY KEY ( `runoob_id` )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    t_type = 'tinyint'


class intField(Template):
    t_type = 'int'


class bigintField(Template):
    t_type = 'bigint'


class floatField(Template):
    t_type = 'float'


class doubleField(Template):
    t_type = 'double'


class datetimeField(Template):
    t_type = 'datetime'


class charField(Template):
    t_type = 'char'


class varcharField(Template):
    t_type = 'varchar'


class textField(Template):
    t_type = 'text'


class tinytextField(Template):
    t_type = 'tinytext'


class longtextField(Template):
    t_type = 'longtext'


def update_field(**kwargs):
    """
    更新字典配置
    """

    def no_rep(key, value, **kwargs):
        """
        不存在则替换
        """
        if key not in kwargs.keys():
            kwargs[key] = value
        return kwargs

    def has_attr(key, **kwargs):
        if key in kwargs.keys():
            return kwargs[key]
        return None

    # kwargs.update(no_rep('table_name', has_attr('__table_name__', **kwargs), **kwargs))
    kwargs.update(no_rep('name', has_attr('name', **kwargs), **kwargs))
    kwargs.update(no_rep('length', has_attr('length', **kwargs), **kwargs))
    kwargs.update(no_rep('d_point', has_attr('d_point', **kwargs), **kwargs))
    kwargs.update(no_rep('t_type', has_attr('t_type', **kwargs), **kwargs))
    kwargs.update(no_rep('is_null', has_attr('is_null', **kwargs), **kwargs))
    kwargs.update(no_rep('primary_key', has_attr('primary_key', **kwargs), **kwargs))
    kwargs.update(no_rep('comment', has_attr('comment', **kwargs), **kwargs))
    kwargs.update(no_rep('auto_field', has_attr('auto_field', **kwargs), **kwargs))
    kwargs.update(no_rep('auto_time', has_attr('auto_time', **kwargs), **kwargs))
    kwargs.update(no_rep('update_auto_time', has_attr('update_auto_time', **kwargs), **kwargs))
    return kwargs
