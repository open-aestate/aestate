import time

from CACodeFramework.cacode.Factory import Factory


class MyFactory(Factory):
    modules = [
        'test.modules.Demo',
        'test.modules.BaseData',
    ]


if __name__ == '__main__':
    t1 = time.time()
    DemoTable = MyFactory.createInstance('Demo.DemoTable')
    count = 0
    result = DemoTable.orm.find().limit(10).end()
    print(result.to_json(True))
    print(time.time() - t1)