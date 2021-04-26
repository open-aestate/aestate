from CACodeFramework.cacode.Factory import Factory


class MyFactory(Factory):
    def __init__(self):
        self.instances = [
            'test.modules.Demo',
            'test.modules.BaseData',
        ]
        super().__init__()


if __name__ == '__main__':
    myFactory = MyFactory()

    ins = myFactory.createInstance("Demo.DemoTable")
    print(ins.FindWheresTIdAndTMsg(t_id=10, t_msg='测试'))
