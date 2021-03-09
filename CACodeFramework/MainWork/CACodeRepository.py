from CACodeFramework.util import DbUtil
import copy


class ParseUtil(object):
    def parse_key(self, *args, to_str=False):
        """
        解析键格式,如:
            INSERT INTO `demo` (这里的就是键) VALUES ('','','','');
        :param args:
        :param to_str:
        :return:
        """
        return self.parse_main(*args, to_str=True, is_key=True)

    def parse_value(self, *args, to_str=False):
        """
        解析值格式,如:
            INSERT INTO `demo` (`index`, `title`, `selects`, `success`) VALUES (这里的就是值);
        :param args:
        :param to_str:
        :return:
        """
        return self.parse_main(*args, to_str=True, is_key=False)

    def parse_insert(self, keys, values, __table_name__):
        field_str = self.parse_key(*keys, to_str=True)
        value_str = self.parse_value(*values, to_str=True)
        return 'INSERT INTO `' + __table_name__ + '` ({}) VALUES({})'.format(field_str, value_str)

    def parse_main(self, *args, to_str=False, is_key):
        """
            解析属性:
                将属性格式设置为:['`a`,','`b`,','`c`']
            :param to_str:是否转成str格式
            :param args:参数
            :return:
        """
        fields = []
        for value in args:
            if is_key:
                fields.append('`' + value + '`' + ',')
            else:
                if type(value) is int:
                    fields.append(str(value) + ',')
                else:
                    fields.append("'" + value + "'" + ',')
        fields[len(fields) - 1] = fields[len(fields) - 1].replace(',', '')
        field_str = ''
        if to_str:
            for field in fields:
                field_str += field
            return field_str
        return fields


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
        # 该对象的所有字段
        self.fields = []
        for key in participants.__dict__.keys():
            self.fields.append(key)
            # 模板类
        self.participants = participants
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
        :return:
        """
        return self.find_by_field(*self.fields)

    def find_by_field(self, *args):
        """
        只查询指定名称的字段,如:
            SELECT user_name FROM `user`
            即可参与仅解析user_name为主的POJO对象
        :param args:需要参与解析的字段名
        :return:
        """
        fields = ParseUtil().parse_key(*args, to_str=True)
        sql = "SELECT {} FROM `{}`".format(fields, self.__table_name__)
        return self.find_many(sql)

    def find_one(self, sql):
        """
        查找第一条数据
            可以是一条
            也可以是很多条中的第一条
        code:
            _result = self.find_many(sql)
            if len(_result) == 0:
                return None
            else:
                return _result[0]
        当前测试中.....
        """
        _result = self.find_many(sql)
        if len(_result) == 0:
            return None
        else:
            return _result[0]

    def find_many(self, sql):
        """
        查询出多行数据
        :param sql:执行的sql语句
        :return:
        """
        _result = self.find_sql(sql=sql)
        _pojo_list = []
        for item in _result:
            pojo = self.parse_obj(item)
            _pojo_list.append(pojo)
        return _pojo_list

    def find_sql(self, sql):
        """
        返回多个数据并用list包装:
            - 可自动化操作
            - 请尽量使用find_many(sql)操作
        :return:注入数据后的实体类
        """
        _result = self.db_util.select_many(sql)
        return _result

    def update(self, sql):
        """
        执行更新操作:
            返回受影响行数
        :param sql:
        :return:
        """
        self.db_util.update(sql=sql)

    def insert_one(self, pojo):
        """
        插入属性:
            返回受影响行数
        :param pojo:POJO类
        :return:
        """
        sql = self.parse_insert(pojo)
        return self.db_util.insert(sql)

    def insert_many(self, pojo_list):
        """
        插入多行
            这个是用insert_one插入多行
        :param pojo_list:
        :return:
        """
        _results = []
        for item in pojo_list:
            _results.append(self.insert_one(item))
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
