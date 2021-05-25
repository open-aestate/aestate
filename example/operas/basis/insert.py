# -*- utf-8 -*-
# @Time: 2021/5/26 1:24
# @Author: CACode
from example.db_base import MyFactory

# 使用自己创建的工厂来创建对象，创建的规则是： `别名`.`类名`
Demo = MyFactory.createInstance('demo.Demo')


def create():
    # 因为我们的模板表设置了`create_time`和`update_time`自动录入时间的`auto_time`和`update_auto_time`
    # 所以这里不需要设置这两个的时间
    # abs参数设置为True时，表示这个对象仅作为数据使用，不参与数据操作过程
    data = MyFactory.createInstance('demo.Demo', name='test_name', password='123456', abs=True)
    # 因为我们在全局配置，也就是db_base.py中的全局配置已经设置了允许返回最后一行的id
    # 所以这里就可以拿到插入后最后一行的id
    # 返回的结果是:受影响行数,最后一行id
    line, last_id = Demo.create(data)
    print(line, last_id)


def save():
    # 为了全局变量的干净，我们得在内部重新创建一个
    Demo = MyFactory.createInstance('demo.Demo')
    # 为对象设置值
    Demo.name = 'test_name'
    Demo.password = '123456'
    # 返回结果,具体参考上一个方法insert()
    line, last_id = Demo.save()
    print(line, last_id)


def insert_sql():
    # TODO: 1.0.0b3 已废弃
    from example.tables import demoModels
    demo = demoModels.Demo()
    line, last_id = demo.insert_sql(sql='INSERT INTO `demo` (`name`,`password`) VALUES ("test_name","test_password")')
    print(line, last_id)


if __name__ == '__main__':
    insert_sql()
