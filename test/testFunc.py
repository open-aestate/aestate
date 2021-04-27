import threading
import time

from CACodeFramework.cacode.Factory import Factory
from test.modules.Demo import DemoTable


class MyFactory(Factory):
    modules = [
        'test.modules.Demo',
        'test.modules.BaseData',
    ]


def setData():
    for i in range(1000):
        DemoTable(t_name=f'测试name{i}', t_pwd=f'测试pwd{i}', t_ms=f'测试msg{i}').save()


if __name__ == '__main__':
    t1 = time.time()
    ins = MyFactory.createInstance("Demo.DemoTable")

    for i in range(10):
        t = threading.Thread(target=setData)
        t.start()

    print(time.time() - t1)
