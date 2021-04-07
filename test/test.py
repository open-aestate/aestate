from enum import Enum

from CACodeFramework.MainWork.CACodePojo import POJO

from CACodeFramework.MainWork.CACodeRepository import Repository

from CACodeFramework.MainWork.Annotations import Table
from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.util import Config, JsonUtil


class ConF(Config.config):
    def __init__(self, host='localhost', port=3306, database='demo', user='root', password='123456', charset='utf8'):
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
class TestClass(Repository):
    def __init__(self):
        super(TestClass, self).__init__(config_obj=ConF(), participants=Demo())


testClass = TestClass()
orm = CACodePureORM(testClass)


def setData():
    for i in range(2):
        h = Demo()
        h.title = "test title"
        h.selects = "test selects"
        h.success = "false"
        _result = testClass.insert_one(pojo=h)
        # _result = orm.insert(h).end()
        print(_result)
    # _result = testClass.insert_many(pojo_list=pojos)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


class table(POJO):
    def __init__(self):
        # 索引
        self.comment_id = None
        # GUID
        self.guid = None
        # 链接
        self.url = None
        # 视图键
        self.view_key = None
        # 商品id
        self.shop_id = None
        # 评论内容
        self.content = None
        # 是否有图片评论
        self.have_img = None
        # 图片地址
        self.img = None
        # 价格
        self.money = None
        # 好评度
        self.success = None
        # 创建时间
        self.create_time = None


class ConF_1(Config.config):
    def __init__(self):
        super(ConF_1, self).__init__(host='localhost', port=3306, database='js_reqs', user='root', password='123456',
                                     charset='utf8', conf={
                'last_id': False,
                'print_sql': True
            })


@Table(name="comments", msg="评论表")
class repo(Repository):
    def __init__(self):
        super(repo, self).__init__(config_obj=ConF_1(), participants=table())


if __name__ == '__main__':
    setData()
    # _all = repo() \
    #     .conversion() \
    #     .find('shop_id', 'count(*)',
    #           asses=[None, 'count'],
    #           h_func=True) \
    #     .group_by('shop_id') \
    #     .append(' having count>1') \
    #     .end()
    # _orm = orm.find('`index`', 'count(*)', asses=[None, 'count'], h_func=True).group_by('index').append(
    #     'having count>1').end()
