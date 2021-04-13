import sys
import threading
import time

from CACodeFramework.MainWork.CACodePojo import POJO

from CACodeFramework.MainWork.CACodeRepository import Repository

from CACodeFramework.MainWork.Annotations import Table, Operations
from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.util import Config, JsonUtil


class ConF(Config.config):
    def __init__(self,
                 host='localhost',
                 port=3306,
                 database='demo',
                 user='root',
                 password='123456',
                 charset='utf8'):
        conf = {
            "print_sql": True,
            "last_id": True,
        }

        super(ConF, self).__init__(host, port, database, user, password, charset, conf=conf)


class Demo(POJO):
    def __init__(self):
        self.index = None
        self.title = None
        self.selects = None
        self.success = None


@Table(name="demo_table", msg="demo message")
# @Operations()
class TestClass(Repository):
    def __init__(self):
        super(TestClass, self).__init__(config_obj=ConF(), participants=Demo())

    def _test(self):
        pass


testClass = TestClass()
orm = CACodePureORM(testClass)


def setData():
    for i in range(2):
        h = Demo()
        h.title = "test title"
        h.selects = "test selects"
        h.success = "false"
        # _result = testClass.insert_one(pojo=h)
        _result = orm.insert(h).end()
        print(_result)
    # _result = testClass.insert_many(pojo_list=pojos)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


def th():
    def A():
        for i in range(10):
            t = TestClass()
            # a = t.conversion().find().end()
            a = t.find_sql(sql='SELECT * FROM demo_table')
            print('id:', t)
            print(a)

    def B():
        for i in range(10):
            t = TestClass()
            b = t.find_many(sql='SELECT * FROM demo_table')
            print(b)

    def C():
        for i in range(10):
            t = TestClass()
            c = t.find_all()
            print(c)

    def D():
        for i in range(10):
            t = TestClass()
            d = t.find_by_field('title', 'selects')
            print(d)

    t1 = time.time()
    # _a = threading.Thread(target=A)
    # _b = threading.Thread(target=B)
    # _c = threading.Thread(target=C)
    _d = threading.Thread(target=D)

    # _a.start()
    # _b.start()
    # _c.start()
    _d.start()

    # _a.join()
    # _b.join()
    # _c.join()
    _d.join()
    t2 = time.time()
    print(t2 - t1)


def copy():
    return testClass.copy()


if __name__ == '__main__':
    # setData()
    # th()
    # print(copy())
    # print(copy())
    _r = orm.find('COUNT(*)', asses=['c'], h_func=True).end()
    print(_r[0].c)
