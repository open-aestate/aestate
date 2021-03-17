import copy

from CACodeFramework.field.sql_fields import *
from CACodeFramework.util import DbUtil


def parse_main(*args, to_str=False, is_field=False):
    """
        解析属性:
            将属性格式设置为:['`a`,','`b`,','`c`']
        :param to_str:是否转成str格式
        :param args:参数
        :param is_field:是否为表字段格式
        :return:
    """
    fields = []
    for value in args:
        if to_str:
            if is_field:
                fields.append('`%s`,' % (str(value)))
        else:
            fields.append(value)
    if len(fields) != 0:
        fields[len(fields) - 1] = fields[len(fields) - 1].replace(',', '')
        field_str = ''
        if to_str:
            for field in fields:
                field_str += field
            return field_str
        return fields
    else:
        return None


class ParseUtil(object):

    def __init__(self, *args, to_str=False, is_field=False):
        """
        初始化解析参数工具
        :param args:需要解析的参数
        :param to_str:是否转成str格式
        :param is_field:是否为表字段格式
        """
        self.args = args
        self.to_str = to_str
        self.is_field = is_field

    def parse_key(self, *args):
        """
        解析键格式,如:
            INSERT INTO `demo` (这里的就是键) VALUES ('','','','');
        :param args:
        :return:
        """
        if args is not None and len(args) != 0:
            self.args = args
        fields = parse_main(*self.args, to_str=True, is_field=True)
        return fields

    def parse_value(self, *args, to_str=False):
        """
        解析值格式,如:
            INSERT INTO `demo` (`index`, `title`, `selects`, `success`) VALUES (这里的就是值);
        :param args:
        :param to_str:
        :return:
        """
        if args is not None:
            self.args = args
        if to_str is not None:
            self.to_str = to_str
        values = parse_main(*self.args, to_str=self.to_str)
        return values

    def parse_insert(self, keys, values, __table_name__):
        fields = self.parse_key(*keys)
        values = self.parse_value(*values)
        # 分析需要几个隐藏值
        hides_value = ''
        for i in range(len(values)):
            hides_value += '%s,'
        # 去除末尾的逗号
        hides_value = hides_value[0: len(hides_value) - 1]
        str(values)
        sql = '%s`%s` (%s)%s(%s)' % (
            insert_str,
            str(__table_name__), fields, values_str, hides_value
        )

        kes = {'sql': sql}
        args = []
        for i in values:
            args.append(i)
        kes['params'] = args
        return kes


class Repository(object):
    """
    - POJO类
        - 继承该类表名此类为数据库的pojo类
        - 需要配合:@Table(name, msg, **kwargs)使用
    """

    def __init__(self, config_obj=None, participants=None):
        """
        初始化配置:
            使用本类需要携带一个来自CACodeFramework.util.Config.config的配置类,详见:CACodeFramework.util.Config.config
        :param config_obj:配置类,继承自CACodeFramework.util.Config.config类
        :param participants:参与解析的对象
        """
        # 移除name和msg键之后,剩下的就是对应的数据库字段
        self.__table_name__ = self.__table_name__
        # 模板类
        self.participants = participants
        # 该对象的所有字段
        self.fields = participants.to_dict().keys()
        # 配置类
        self.config_obj = config_obj
        # 操作数据库
        self.db_util = DbUtil.Db_opera(host=self.config_obj.host,
                                       port=self.config_obj.port,
                                       user=self.config_obj.user,
                                       password=self.config_obj.password,
                                       database=self.config_obj.database,
                                       charset=self.config_obj.charset)

    def find_all(self):
        """
        查询所有
        :return:将所有数据封装成POJO对象并返回
        """
        return self.find_by_field(*self.fields)

    def find_by_field(self, *args):
        """
        只查询指定名称的字段,如:
            SELECT user_name FROM `user`
            即可参与仅解析user_name为主的POJO对象
        :param args:需要参与解析的字段名
        :return:将所有数据封装成POJO对象并返回
        """
        fields = ParseUtil(*args, is_field=True).parse_key()
        sql_str = find_str + fields + from_str + self.__table_name__
        return self.find_many(sql=sql_str)

    def find_one(self, **kwargs):
        """
        查找第一条数据
            可以是一条
            也可以是很多条中的第一条
        code:
            _result = self.find_many(**kwargs)
            if len(_result) == 0:
                return None
            else:
                return _result[0]
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        :return 返回使用find_many()的结果种第一条
        """
        kwargs = self.print_sql(**kwargs)
        _result = self.find_many(**kwargs)
        if len(_result) == 0:
            return None
        else:
            return _result[0]

    def find_many(self, **kwargs):
        """
        查询出多行数据
            第一个必须放置sql语句
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        :return 将所有数据封装成POJO对象并返回
        """
        kwargs = self.print_sql(**kwargs)
        _result = self.find_sql(**kwargs)
        _pojo_list = []
        for item in _result:
            pojo = self.parse_obj(item)
            _pojo_list.append(pojo)
        return _pojo_list

    def find_sql(self, **kwargs):
        """
        返回多个数据并用list包装:
            - 可自动化操作
            - 请尽量使用find_many(sql)操作
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        """
        kwargs = self.print_sql(**kwargs)
        return self.db_util.select(**kwargs)

    def update(self, **kwargs):
        """
        执行更新操作:
            返回受影响行数
        pass:
            删除也是更新操做
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :return:
        """
        kwargs = self.print_sql(**kwargs)
        kwargs = self.last_id(**kwargs)
        return self.db_util.update(**kwargs)

    def insert_sql(self, **kwargs):
        """
        使用sql插入
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :return rowcount,last_id if last_id=True
        """
        kwargs = self.print_sql(**kwargs)
        kwargs = self.last_id(**kwargs)
        return self.db_util.insert(**kwargs)

    def insert_one(self, **kwargs):
        """
        插入属性:
            返回受影响行数
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            params:需要填充的字段
        :return:rowcount,last_id if last_id=True
        """
        kwargs = self.print_sql(**kwargs)
        kwargs = self.last_id(**kwargs)
        _result = self.parse_insert(kwargs['pojo'])
        kwargs['sql'] = _result['sql']
        kwargs['params'] = _result['params']
        return self.db_util.insert(**kwargs)

    def insert_many(self, **kwargs):
        """
        插入多行
            这个是用insert_one插入多行
        :param kwargs:包含所有参数:
            pojo_list:参照对象列表
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :return:list[rowcount,last_id if last_id=True]
        """
        kwargs = self.print_sql(**kwargs)
        kwargs = self.last_id(**kwargs)
        _results = []
        for item in kwargs['pojo_list']:
            kwargs['pojo'] = item
            _results.append(self.insert_one(**kwargs))
        return _results

    def parse_obj(self, data: dict):
        """
        将数据解析成对象
        注意事项:
            数据来源必须是DbUtil下查询出来的
        :param data:单行数据
        :return:POJO对象
        """
        # 深度复制对象
        part_obj = copy.deepcopy(self.participants)
        for key, value in data.items():
            setattr(part_obj, key, value)
        return part_obj

    def parse_insert(self, pojo):
        """
        解析插入语句
        :param pojo:
        :return:
        """
        _dict = pojo.__dict__
        keys = []
        values = []
        for key, value in _dict.items():
            if value is None:
                continue
            keys.append(key)
            values.append(value)
        return ParseUtil().parse_insert(keys, values, self.__table_name__)

    def get_this(self):
        """
        获取当前仓库
        """
        return self

    def get_conf(self):
        """
        获取当前配置项
        """
        return self.config_obj

    def print_sql(self, **kwargs):
        """
        基本功死亡区:
        遵循规则：
            内部>配置文件
        是否包含打印sql的配置
        存在于所有数据库操做
        """
        if 'print_sql' not in kwargs.keys():
            if 'print_sql' in self.config_obj.conf.keys():
                kwargs['print_sql'] = self.config_obj.conf['print_sql']
        return kwargs

    def last_id(self, **kwargs):
        """
        基本功死亡区:
        遵循规则：
            内部>配置文件
        是否包含返回最后一行ID的配置
        只存在于更新操做的方法内，如：
            insert,
            update,
            delete
        """
        if 'last_id' not in kwargs.keys():
            if 'last_id' in self.config_obj.conf.keys():
                kwargs['last_id'] = self.config_obj.conf['last_id']
        return kwargs
