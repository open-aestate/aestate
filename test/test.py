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
        self.set_field('print_sql', True)
        self.set_field('last_id', True)

        super(ConF, self).__init__(host, port, database, user, password, charset)


def Before(**kwargs):
    print('Before:', kwargs)


def After(*args, **kwargs):
    print('After', args)
    print('Result:', kwargs)


# @Table(name="demo_table", msg="demo message")
class demo_table(Manage.Pojo):
    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField(primary_key=True)
        self.t_name = Manage.tag.varcharField(length=255)
        self.t_pwd = Manage.tag.varcharField(length=255)
        self.t_msg = Manage.tag.varcharField(length=255)
        self.create_time = Manage.tag.datetimeField(auto_time=True)
        self.update_time = Manage.tag.datetimeField(update_auto_time=True)

        super(demo_table, self).__init__(config_obj=ConF(), **kwargs)

    @AopModel(before=Before, before_kwargs={'1': '1'}, after=After)
    def find_title_and_selects(self, **kwargs):
        print('function task', kwargs['uid'])
        _r = self.orm.find().end()
        print(_r)
        return _r

    @Select(sql="SELECT COUNT(*) FROM demo_table WHERE t_id<=%s AND t_msg like %s", params=[10, '${t_msg}'])
    class find_all_where_tid_and_t_msg:
        def __init__(self, t_id, t_msg):
            self.t_id = t_id
            self.t_msg = t_msg
            self.meta = demo_table


def setData():
    end = demo_table().orm.find().order_by('t_id').desc().limit(1).first().end()
    for i in range(end.t_id, 100000 * end.t_id):
        demo_table(t_name='{}{}'.format('测试name', i), t_pwd='{}{}'.format('测试pwd', i),
                   t_msg='{}{}'.format('测试msg', i)).save()
        # a.append(h)
        # _result = testClass.insert_one(pojo=h)
    # _r = demo_table().orm.insert(h).end()
    # h.insert_many(pojo_list=a)
    # _result = testClass.insert_many(pojo_list=pojos)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


data_count = 0


def th():
    def A():
        for i in range(100):
            demo_table(t_name='test_name', t_pwd='123', t_msg='123').save()

    a = threading.Thread(target=A)
    return a


if __name__ == '__main__':
    # setData()
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
    d = demo_table()
    f = d.__fields__
    result = d.find_all_where_tid_and_t_msg(t_id=10, t_msg='%测试msg%')
    print(result)
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
