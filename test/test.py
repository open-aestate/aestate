import threading
import uuid

from CACodeFramework.anno.annos import Table, Select
from CACodeFramework.anno.aop import AopModel
from CACodeFramework.pojoManager import Manage

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


def Before(**kwargs):
    print('Before:', kwargs)


def After(*args, **kwargs):
    print('After', args)
    print('Result:', kwargs)


@Table(name="demo_table", msg="demo message")
class demo_table(Manage.Pojo):
    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField(primary_key=True)
        self.t_name = Manage.tag.varcharField(length=255)
        self.t_pwd = Manage.tag.varcharField(length=255)
        self.t_msg = Manage.tag.varcharField(length=255)
        self.create_time = Manage.tag.datetimeField(auto_time=True)
        self.update_time = Manage.tag.datetimeField(update_auto_time=True)

        super(demo_table, self).__init__(config_obj=ConF(), close_log=True, **kwargs)

    @AopModel(before=Before, before_kwargs={'1': '1'}, after=After)
    def find_title_and_selects(self, **kwargs):
        print('function task', kwargs['uid'])
        _r = self.orm.find().end()
        print(_r)
        return _r

    @Select(sql='SELECT * FROM demo_table WHERE t_id=%s', params=[1])
    class find_all_where_tid(Manage.Operation):
        def __init__(self, t_id):
            self.t_id = t_id

        def meta(self):
            return demo_table()


def setData():
    a = []
    h = demo_table()
    for i in range(1000):
        h = demo_table(t_name='{}{}'.format('测试name', i), t_pwd='{}{}'.format('测试pwd', i),
                       t_msg='{}{}'.format('测试msg', i))
        # a.append(h)
        h.save()
        # _result = testClass.insert_one(pojo=h)
    # _r = demo_table().orm.insert(h).end()
    # h.insert_many(pojo_list=a)
    # _result = testClass.insert_many(pojo_list=pojos)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


data_count = 0


def th():
    def A():
        for i in range(100):
            d = demo_table()
            a = d.find_sql(sql='SELECT * FROM demo_table')
            global data_count
            data_count += len(a)

    def B():
        for i in range(100):
            b = demo_table().find_many(sql='SELECT * FROM demo_table')
            global data_count
            data_count += len(b)

    def C():
        for i in range(100):
            c = demo_table().find_all()
            global data_count
            data_count += len(c)

    def D():
        for i in range(100):
            d = demo_table().find_by_field('title', 'selects')
            global data_count
            data_count += len(d)

    _a = threading.Thread(target=A)
    _b = threading.Thread(target=B)
    _c = threading.Thread(target=C)
    _d = threading.Thread(target=D)
    return _a, _b, _c, _d


if __name__ == '__main__':
    setData()
    # c = demo_table().orm.find('count(*)', asses=['c'], h_func=True).end()[0]
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
    # d = demo_table()
    # u = uuid.uuid1()
    # result = d.find_title_and_selects(uid=u)
    # print(JsonUtil.parse(result, True))
    # a = d.find_all_where_tid(1).run()
    # print(a)
    # re = d.orm.find('t_id', 't_name', 't_pwd').where(t_id="<<10").first().end()
    # print(re.to_json(True))
    # d.before_find_title_and_selects(*d.before_args_find_title_and_selects,
    #                                 **d.before_kwargs_find_title_and_selects)
    # _r = d.orm.update().set(success='true').where(index=17034).end()
    # print(_r)
