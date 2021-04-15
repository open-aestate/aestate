import threading
import time

from CACodeFramework.util.Log import CACodeLog

from CACodeFramework.MainWork import CACodePojo

from CACodeFramework.MainWork.Annotations import Table
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


@Table(name="demo_table", msg="demo message")
class Demo(CACodePojo.POJO):
    def __init__(self, **kwargs):
        self.index = CACodePojo.intField(name='index', primary_key=True)
        self.title = CACodePojo.varcharField(length=255)
        self.selects = CACodePojo.varcharField(length=255)
        self.success = CACodePojo.varcharField(length=255)
        super(Demo, self).__init__(config_obj=ConF(), close_log=True, **kwargs)


def setData():
    a = []
    h = Demo()
    for i in range(2):
        h = Demo(title="test title", selects="test selects", success='false')
        a.append(h)
        # _result = testClass.insert_one(pojo=h)
        _r = Demo().orm.insert(h).end()
    # h.insert_many(pojo_list=a)
    # _result = testClass.insert_many(pojo_list=pojos)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


data_count = 0


def th():
    def A():
        for i in range(100):
            d = Demo()
            a = d.find_sql(sql='SELECT * FROM demo_table')
            global data_count
            data_count += len(a)

    def B():
        for i in range(100):
            b = Demo().find_many(sql='SELECT * FROM demo_table')
            global data_count
            data_count += len(b)

    def C():
        for i in range(100):
            c = Demo().find_all()
            global data_count
            data_count += len(c)

    def D():
        for i in range(100):
            d = Demo().find_by_field('title', 'selects')
            global data_count
            data_count += len(d)

    _a = threading.Thread(target=A)
    _b = threading.Thread(target=B)
    _c = threading.Thread(target=C)
    _d = threading.Thread(target=D)
    return _a, _b, _c, _d


if __name__ == '__main__':
    # setData()
    # c = Demo().orm.find('count(*)', asses=['c'], h_func=True).end()[0]
    # print('count:', c.c)
    # t1 = time.time()
    # t = th()
    # for i in t:
    #     i.start()
    #     i.join()
    # t2 = time.time()
    # print('time:', t2 - t1)
    # print('data count:', data_count)
    # print('average:', data_count / (t2 - t1))

    _r = Demo().orm.update().set(success='true').where(index=17036).end()
    print(_r)
