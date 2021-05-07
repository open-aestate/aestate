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
    for i in range(10):
        a.append(MyFactory.createInstance('SqlServerTest.DemoTable', t_msg='测试msg'))
    return a


info = CACodeLog.log
warn = CACodeLog.warning


def TestMySql():
    t1 = time.time()
    demoTable = MyFactory.createInstance('MySqlTest.DemoTable')
    demoTable.config_obj.insert(demoTable.__table_name__, demoTable.__fields__)
    # result = demoTable.find_all()
    result = demoTable.create(pojo=set_many(), many=True)
    info(f'time:{time.time() - t1}')
    info(f'count:{len(result)}')
    warn(result)


def TestSqlServer():
    testCCFK = MyFactory.createInstance('SqlServerTest.DemoTable')
    result = testCCFK.create(pojo=set_many(), many=True)
    info(result)


if __name__ == '__main__':
    # TestSqlServer()
    TestMySql()
