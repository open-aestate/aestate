from CACodeFramework.MainWork import CACodeRepository, CACodePojo
from CACodeFramework.MainWork.Annotations import Table
from CACodeFramework.util import Config, JsonUtil


class ConF(Config.config):
    def __init__(self, host='localhost', port=3306, database='demo', user='root', password='123456', charset='utf8'):
        super(ConF, self).__init__(host, port,
                                   database, user, password, charset)


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
    for i in range(1, 1000):
        h = Demo()
        h.index = i
        h.title = "test title"
        h.selects = "test selects"
        h.success = "false"
        testClass = TestClass()
        _result = testClass.insert_one(h)
        print('受影响行数：{}\t,\t已插入：{}'.format(_result, i))


if __name__ == '__main__':
    import time

    # setData()
    star_time = time.time()
    testClass = TestClass()
    _result = testClass.update('DELETE FROM demo_table')
    end_time = time.time()
    print(end_time - star_time)
