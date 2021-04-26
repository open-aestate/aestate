from CACodeFramework.cacode.Factory import Factory


class MyFactory(Factory):
    modules = [
        'test.modules.Demo',
        'test.modules.BaseData',
    ]


if __name__ == '__main__':
    ins = MyFactory.createInstance("Demo.DemoTable")
    ins_2 = MyFactory.createInstance("Demo.DemoTable")
    result = ins.FindAllWhereTID(t_id=10)
    # result = ins.orm.find('t_id', 't_msg').end().to_json()
    print(result.to_json(True))
    result = ins.FindWheresTIdAndTMsg(t_id='测', t_msg='试')
    # result = ins.find_all()
    print(result.page(2))
