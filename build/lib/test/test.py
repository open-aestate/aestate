import time

from CACodeFramework.MainWork import CACodeRepository, CACodePojo
from CACodeFramework.MainWork.Annotations import Table
from CACodeFramework.util import Config


class ConF(Config.config):
    def __init__(self, host='localhost', port=3306, database='demo', user='root', password='123456', charset='utf8'):
        super(ConF, self).__init__(host, port, database, user, password, charset)


@Table(name="demo_table", msg="demo message")
class TestClass(CACodeRepository.Repository):
    def __init__(self):
        super(TestClass, self).__init__(config_obj=ConF(), participants=Demo())


class Demo(CACodePojo.POJO):
    def __init__(self):
        self.index = None
        self.title = None
        self.selects = None
        self.success = None


def setData():
    h = Demo()
    h.title = "test title"
    h.selects = "test selects"
    h.success = "false"
    h1 = Demo()
    h1.title = "test title"
    h1.selects = "test selects"
    h1.success = "false"
    testClass = TestClass()
    _result = testClass.insert_many([h, h1])
    print(_result)
    # print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


if __name__ == '__main__':
    setData()
    # testClass = TestClass()
    # _result = testClass.find_many('SELECT count(*) as count FROM demo_table')
    # for i in _result:
    #     print(i.__dict__)
