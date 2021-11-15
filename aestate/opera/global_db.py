import sys

from aestate.exception import MySqlErrorTest
from aestate.util.Log import ALog
from aestate.opera.DBPool.pooled_db import PooledDB


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
        # 是否执行多条sql
        many_flay = 'many' in kwargs.keys() and kwargs['many']
        if 'print_sql' in kwargs.keys() and kwargs['print_sql'] is True:
            _l = sys._getframe().f_back.f_lineno
            msg = f'{kwargs["sql"]} - many=True' if many_flay else kwargs['sql']
            ALog.log(obj=db, line=_l, task_name='Print Sql', msg=msg)
        if many_flay:
            cursor.executemany(kwargs['sql'], kwargs['params'])
        else:
            if 'params' in kwargs and kwargs['params']:
                cursor.execute(kwargs['sql'], tuple(kwargs['params']))
            else:
                cursor.execute(kwargs['sql'])
            # try:
            #     CACodeLog.log(obj=db, line=_l, task_name='Print Sql', msg=cursor._executed)
            # except:
            #     CACodeLog.log(obj=db, line=_l, task_name='Print Sql', msg=msg)
        return cursor
    except Exception as e:
        db.rollback()
        mysql_err = MySqlErrorTest(e)
        mysql_err.ver()
        mysql_err.raise_exception()


class Db_opera(PooledDB):
    def __init__(self, *args, **kwargs):
        if 'POOL' not in kwargs or kwargs['POOL'] is None:
            self.POOL = self
        if 'POOL' in kwargs.keys():
            kwargs.pop('POOL')

        super(Db_opera, self).__init__(*args, **kwargs)

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
        try:
            cursor = parse_kwa(db=db, **kwargs)
            # 列名
            col = cursor.description
            data = cursor.fetchall()
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
        try:
            cursor = parse_kwa(db=db, many=many, **kwargs)
            db.commit()
            # 受影响行数
            rowcount = cursor.rowcount
            # 返回受影响行数
            if kwargs['last_id']:
                return rowcount, cursor.lastrowid
            else:
                return rowcount
        except Exception as e:
            db.rollback()
            raise e
        finally:
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
