class baseTag(object):
    def __init__(self, table_name=None,
                 name=None,
                 length=None,
                 d_point=None,
                 t_type='varchar',
                 is_null=False,
                 primary_key=False,
                 comment="",
                 auto_field=False,
                 auto_time=False,
                 update_auto_time=False):
        """
        :param table_name:表名称
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
        """
        self.update_auto_time = update_auto_time
        self.auto_time = auto_time
        self.autoField = auto_field
        self.table_name = table_name
        self.comment = comment
        self.primary_key = primary_key
        self.is_null = is_null
        self.d_point = d_point
        self.name = name
        self.t_type = t_type
        self.length = length

    def get_table(self):
        """
        获取表数据结构
        """
        return self.__dict__
