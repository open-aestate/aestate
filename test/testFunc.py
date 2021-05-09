'''
Author: CACode
Date: 2021-04-26 11:46:16
LastEditTime: 2021-05-08 15:41:38
LastEditors: Please set LastEditors
Description: Update Test
'''
import time

from CACodeFramework.cacode.Factory import Factory
from CACodeFramework.util.Log import CACodeLog


class MyFactory(Factory):
    modules = [
        'test.modules.Demo',
        'test.modules.MySqlTest',
        'test.modules.SqlServerTest',
    ]


def set_many():
    a = []
    for i in range(0, 1):
        a.append(
            MyFactory.createInstance('MySqlTest.DemoTable', t_msg=f'测试msg{i}', t_name=f'测试name{i}', t_pwd=f'测试pwd{i}',
                                     abs=True))
    return a


def TestMySql():
    demoTable = MyFactory.createInstance('MySqlTest.DemoTable')
    # result = demoTable.find_all()
    test_data = set_many()
    t = time.time()
    result = demoTable.create(pojo=test_data, many=True)
    # result = demoTable.find_by_id(t_id=10)
    # page = result.page(7)
    # r = page.to_dict()
    # r = demoTable.orm.find().where(t_msg__fuck='1').end()
    info(result)
    # info(f'count:{len(result)}')
    info(f'application run time:{time.time() - t}')
    # warn(result)


def TestSqlServer():
    testCCFK = MyFactory.createInstance('SqlServerTest.DemoTable')
    result = testCCFK.create(pojo=set_many(), many=True)
    info(result)


if __name__ == '__main__':
    info = CACodeLog.log
    warn = CACodeLog.warning
    t1 = time.time()
    # TestSqlServer()
    TestMySql()
    info(f'time:{time.time() - t1}')
