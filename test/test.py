from enum import Enum

from CACodeFramework.MainWork import CACodeRepository, CACodePojo
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


class Demo(CACodePojo.POJO):
    def __init__(self):
        self.index = None
        self.title = None
        self.selects = None
        self.success = None


@Table(name="demo_table", msg="demo message")
class TestClass(CACodeRepository.Repository):
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


if __name__ == '__main__':
    setData()

    # _orm = orm.find('`index`', 'count(*)', asses=[None, 'count'], h_func=True).group_by('index').append(
    #     'having count>1').end()
