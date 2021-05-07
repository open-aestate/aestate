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
    for i in range(100):
        a.append(MyFactory.createInstance('SqlServerTest.DemoTable', t_msg='测试msg', abs=True))
    return a


info = CACodeLog.log
warn = CACodeLog.warning


def TestMySql():
    demoTable = MyFactory.createInstance('MySqlTest.DemoTable')
    # result = demoTable.find_all()
    test_data = set_many()

    # result = demoTable.create(pojo=test_data, many=True)
    result = demoTable.find_all()

    info(f'count:{len(test_data)}')
    warn(result)


def TestSqlServer():
    testCCFK = MyFactory.createInstance('SqlServerTest.DemoTable')
    result = testCCFK.create(pojo=set_many(), many=True)
    info(result)


if __name__ == '__main__':
    t1 = time.time()
    TestSqlServer()
    # TestMySql()
    info(f'time:{time.time() - t1}')
