'''
Author: CACode
Date: 2021-04-26 11:46:16
LastEditTime: 2021-05-08 15:41:38
LastEditors: Please set LastEditors
Description: Update Test
'''
import time
from datetime import datetime

from aestate.cacode.Factory import Factory
from aestate.util.Log import CACodeLog


class MyFactory(Factory):
    modules = {
        "demo": 'test.modules.Demo',
        "mysql_test": 'test.modules.MySqlTest',
        "sqlserver_test": 'test.modules.SqlServerTest',
    }


def set_many():
    a = []
    for i in range(0, 1):
        a.append(
            MyFactory.createInstance('sqlserver_test.DemoTable', t_msg=f'测试msg{i}', t_name=f'测试name{i}',
                                     t_pwd=f'测试pwd{i}', create_time=datetime.utcnow(),
                                     abst=True))
    return a


def TestMySql():
    demoTable = MyFactory.createInstance('mysql_test.DemoTable')
    demoTable = MyFactory.createInstance('mysql_test.De')
    # result = demoTable.find_all()
    test_data = set_many()
    t = time.time()
    # result = demoTable.find_field('t_id')
    # result = demoTable.create(pojo=test_data, many=True)
    # result = demoTable.orm.find().where(t_id=10).end()
    # page = result.page(7)
    # result = page.to_dict()
    # result = demoTable.orm.find().where(t_id__eq=10).end()
    # result = demoTable.orm.find().where(t_id=1, t_name='测试name0').end()
    # result = demoTable.orm.find().where(t_id='<<10', t_name='测试name0').end()
    result = demoTable.orm.find().where(t_id='>>10', t_name='测试name10').end()
    # result.add_field('aaaa', True)
    # result.remove_field('t_id')
    # r_2 = d_2.orm.find(poly=[' FROM '])
    # var = r_2 << result
    info(result)
    # info(result.to_json(True))
    # info(f'count:{len(result)}')
    info(f'application run time:{time.time() - t}')
    # warn(result)


def TestSqlServer():
    testCCFK = MyFactory.createInstance('SqlServerTest.DemoTable')
    result = testCCFK.create(pojo=set_many(), many=True)
    info(result)


def me():
    print(time.time())


if __name__ == '__main__':
    info = CACodeLog.log
    warn = CACodeLog.warning
    t1 = time.time()
    # TestSqlServer()
    TestMySql()
    info(f'time:{time.time() - t1}')
    # me()
