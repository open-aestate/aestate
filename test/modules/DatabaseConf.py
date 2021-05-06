import pymysql

from CACodeFramework.util import Config


class ConF(Config.config):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 database='demo',
                 user='root',
                 password='123456',
                 charset='utf8'):
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(ConF, self).__init__(host, port, database, user, password, charset, creator=pymysql)


class DemoConF(Config.config):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 database='demo',
                 user='root',
                 password='123456',
                 charset='utf8'):
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(DemoConF, self).__init__(host, port, database, user, password, charset, creator=pymysql)
