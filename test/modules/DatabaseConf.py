import pymssql
import pymysql

from CACodeFramework.util import Config


class MySqlConfig(Config.config):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 database='demo',
                 user='root',
                 password='123456',
                 charset='utf8'):
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(MySqlConfig, self).__init__(host, port, database, user, password, charset, creator=pymysql)


class SqlServerConfig(Config.config):
    def __init__(self,
                 host='106.55.92.201',
                 port=1433,
                 database='test',
                 user='sa',
                 password='Zyzs1234..',
                 charset='utf8'):
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(SqlServerConfig, self).__init__(host, port, database, user, password, charset, creator=pymssql)
