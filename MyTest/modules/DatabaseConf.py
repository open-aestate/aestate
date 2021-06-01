import pymssql
import pymysql

from aestate.work import Config
from aestate.work.SummerAdapter import LanguageAdapter


class Adapter(LanguageAdapter):
    def __init__(self):
        self.funcs = {
            'fuck': self.__fuck
        }
        super(Adapter, self).__init__()

    def __fuck(self, instance, key, value):
        self._like_opera(instance, key, value)


class MySqlConfig(Config.Conf):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 database='demo',
                 user='root',
                 password='123456',
                 charset='utf8'):
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(MySqlConfig, self).__init__(host, port, database, user, password, charset, creator=pymysql,
                                          adapter=Adapter())


class SqlServerConfig(Config.Conf):
    def __init__(self,
                 host='localhsot',
                 port=1433,
                 database='test',
                 user='sa',
                 password='123456',
                 charset='utf8'):
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(SqlServerConfig, self).__init__(host, port,
                                              database, user, password, charset, creator=pymssql)

    def parse_insert(self, keys, values, __table_name__, insert_str, values_str, symbol='%s',
                     sql_format='%s [%s] (%s)%s(%s)'):
        return super(SqlServerConfig, self).parse_insert(keys, values, __table_name__, insert_str, values_str, symbol,
                                                         sql_format)

    def parse_main(self, *args, to_str=False, is_field=False, symbol='%s'):
        """
            解析属性:
                将属性格式设置为:['`a`,','`b`,','`c`']
            :param to_str:是否转成str格式
            :param args:参数
            :param is_field:是否为表字段格式
            :param symbol:分隔符语法
            :return:
        """
        fields = []
        for value in args:
            if to_str:
                if is_field:
                    fields.append(f'[{symbol}],' % (str(value)))
                else:
                    fields.append(f'{symbol},' % (str(value)))
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
