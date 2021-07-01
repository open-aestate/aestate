from example.tables.demoModels import DemoTable


def test_check():
    checkout = DemoTable().orm.check()


if __name__ == '__main__':
    test_check()
