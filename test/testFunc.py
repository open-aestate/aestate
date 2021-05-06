import time

from CACodeFramework.cacode.Factory import Factory
from CACodeFramework.util.Log import CACodeLog
from test.modules.DemoTable import DemoTable


class MyFactory(Factory):
    modules = [
        'test.modules.Demo',
        'test.modules.DemoTable',
    ]


def set_many():
    a = []
    for i in range(10):
        a.append(DemoTable(t_name='测试name', t_msg='测试msg', t_pwd='测试pwd'))
    return a


info = CACodeLog.log
warn = CACodeLog.warning

if __name__ == '__main__':
    t1 = time.time()
    demoTable = MyFactory.createInstance('DemoTable.DemoTable')
    count = 0
    # result = demoTable.find_all()
    result = demoTable.create(pojo=set_many(), many=True)
    info(f'time:{time.time() - t1}')
    info(f'count:{len(result)}')
    warn(result)
