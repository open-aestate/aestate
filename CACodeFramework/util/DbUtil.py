import sys
import threading

from CACodeFramework.cacode.Modes import Singleton
from CACodeFramework.util.DBPool.pooled_db import PooledDB
from CACodeFramework.util.Log import CACodeLog


def parse_kwa(db, **kwargs):
    """
    解析并执行sql

    :param db:db_util对象
    :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
            many:是否有多个
    """

    try:
        cursor = db.cursor()
        many_flay = 'many' in kwargs.keys() and kwargs['many']
        # if 'params' in kwargs.keys():
        #     sql = cursor.mogrify(kwargs['sql'], kwargs['params'])
        # else:
        #     sql = kwargs['sql']
        if 'print_sql' in kwargs.keys() and kwargs['print_sql'] is True:
            _l = sys._getframe().f_back.f_lineno
            msg = f'{kwargs["sql"]} - many=True' if many_flay else kwargs['sql']
            CACodeLog.log(obj=db, line=_l, task_name='Print Sql', msg=msg)

        if many_flay:
            cursor.executemany(kwargs['sql'], kwargs['pojo_data'])
        else:
            cursor.execute(kwargs['sql'], tuple(kwargs['params']))
        return cursor
    except Exception as e:
        db.rollback()
        raise e


class Db_opera(object):
    """


    """

    _instance_lock = threading.Lock()

    def __init__(self, host, port, user, password, database, charset='utf8', creator=None, maxconnections=6,
                 mincached=2,
                 maxcached=5, maxshared=3, blocking=True, setsession=[], ping=0, POOL=None):
        """

        设置DB-API 2连接池。

        creator：返回新的DB-API 2的任意函数
            连接对象或符合DB-API 2的数据库模块
        mincached：池中空闲连接的初始数量
            （0表示启动时未建立连接）
        maxcached：池中最大空闲连接数
            （0或无表示池大小不受限制）
        maxshared：共享连接的最大数量
            （0或无表示所有连接都是专用的）
            当达到此最大数量时，连接为
            如果被要求共享，则将它们共享。
        maxconnections：通常允许的最大连接数
            （0或无表示任意数量的连接）
        blocking：确定超出最大值时的行为
            （如果将其设置为true，请阻止并等待，直到
            连接减少，否则将报告错误）
        maxusage：单个连接的最大重用次数
            （0或无表示无限重用）
            当达到连接的最大使用次数时，
            连接将自动重置（关闭并重新打开）。
        setsession：可用于准备的SQL命令的可选列表
            会话，例如[“将日期样式设置为...”，“将时区设置为...”]
        reset：返回到池后应如何重置连接
            （对于以begin（）开始的回滚事务，为False或None，
            出于安全考虑，总是发出回滚是正确的）
        failures：可选的异常类或异常类的元组
            为此，应应用连接故障转移机制，
            如果默认值（OperationalError，InternalError）不足够
        ping：确定何时应使用ping（）检查连接
            （0 =无=永不，1 =默认=每当从池中获取时，
            2 =创建游标时，4 =执行查询时，
            7 =始终，以及这些值的所有其他位组合）
        args，kwargs：应传递给创建者的参数
            函数或DB-API 2模块的连接构造函数


        初始化配置
        以下参数与PooledDB一致
        :param creator:默认即可
        :param maxconnections:默认即可
        :param mincached:默认即可
        :param maxcached:默认即可
        :param maxshared:默认即可
        :param blocking:默认即可
        :param setsession:默认即可
        :param ping:默认即可
        :param host:数据库IP地址
        :param port:端口
        :param user:用户名,如root
        :param password:密码
        :param database:数据库名
        :param charset:编码格式
        :param POOL:使用自定义的PooledDB,不建议
        """
        self.creator = creator
        self.maxconnections = maxconnections
        self.mincached = mincached
        self.maxcached = maxcached
        self.maxshared = maxshared
        self.blocking = blocking
        self.setsession = setsession
        self.ping = ping
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.POOL = POOL
        self.init_config()

    def init_config(self):
        """
        初始化数据库连接池
        """
        if self.POOL is None:
            self.POOL = PooledDB(creator=self.creator, maxconnections=self.maxconnections, mincached=self.mincached,
                                 maxcached=self.maxcached,
                                 maxshared=self.maxshared,
                                 blocking=self.blocking,
                                 setsession=self.setsession,
                                 ping=0, host=self.host, port=self.port,
                                 user=self.user,
                                 password=self.password, database=self.database, charset=self.charset)

    def get_conn(self):
        """
        获取数据库连接池
        :return:
        """
        return self.POOL.connection()

    def select(self, **kwargs):
        """
        查找多个
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        :return:
        """
        db = self.get_conn()
        cursor = None
        try:
            cursor = parse_kwa(db=db, **kwargs)
            # 列名
            col = cursor.description
            data = []
            while True:
                one = cursor.fetchone()
                if one is None:
                    break
                else:
                    data.append(one)
            db.close()
            _result = []
            for data_index, data_value in enumerate(data):
                _messy = {}
                for item_index, item_value in enumerate(data_value):
                    _messy[col[item_index][0]] = item_value
                _result.append(_messy)
            return _result
        except Exception as e:
            db.rollback()
            raise e
        finally:
            if not cursor:
                cursor.close()
            db.close()

    def insert(self, many=False, **kwargs):
        """
        执行插入语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :param many:是否为多行执行
        """
        db = self.get_conn()
        cursor = None
        try:
            cursor = parse_kwa(db=db, many=many, **kwargs)
            db.commit()
            # 最后一行ID
            last = cursor.lastrowid
            # 受影响行数
            rowcount = cursor.rowcount
            # 返回受影响行数
            if kwargs['last_id']:
                return rowcount, last
            else:
                return rowcount
        except Exception as e:
            db.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            db.close()

    def update(self, **kwargs):
        """
        执行更新语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        return self.insert(**kwargs)

    def delete(self, **kwargs):
        """
        执行删除语句
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        """
        self.insert(**kwargs)

    def __new__(cls, *args, **kwargs):

        # if Db_opera.instance is None:
        #     Db_opera.instance = object.__new__(cls)
        # return Db_opera.instance
        instance = Singleton.createDbOpera(cls)
        return instance
