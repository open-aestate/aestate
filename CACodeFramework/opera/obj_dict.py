from CACodeFramework.util.ParseUtil import ParseUtil


class parses(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def last_id(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        遵循规则：

            内部>配置文件

        是否包含返回最后一行ID的配置

        只存在于更新操做的方法内，如：

            insert,

            update,

            delete

         Attributes:

             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'last_id' not in kwargs.keys():
            if 'last_id' in conf_obj.conf.keys():
                kwargs['last_id'] = conf_obj.conf['last_id']
            else:
                kwargs['last_id'] = False
        return kwargs

    def print_sql(self, **kwargs):
        """
        遵循规则：
            内部>配置文件

        是否包含打印sql的配置

        存在于所有数据库操做

        Attributes:
             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'print_sql' not in kwargs.keys():
            if 'print_sql' in conf_obj.conf.keys():
                kwargs['print_sql'] = conf_obj.conf['print_sql']
            else:
                kwargs['print_sql'] = False
        return kwargs

    def parse_insert(self, pojo, __table_name__):
        """
        解析插入语句

        INSERT INTO `__table_name__`(`title`,'selects') VALUE ('','')

        :param pojo:POJO对象
        :param __table_name__:表名
        :return:
        """
        _dict = pojo.fields
        # 得到所有的键
        keys = pojo.fields
        # 在得到值之后解析是否为空并删除为空的值和对应的字段
        cp_value = []
        # 复制新的一张字段信息
        keys_copy = []

        values = [getattr(pojo, v) for v in keys]
        for i, j in enumerate(values):
            if j is not None and not pojo.is_default(j):
                keys_copy.append(keys[i])
                cp_value.append(j)
        return ParseUtil().parse_insert(keys_copy, cp_value, __table_name__)
