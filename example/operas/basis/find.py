# -*- utf-8 -*-
# @Time: 2021/5/25 0:33
# @Author: CACode
from example.db_base import MyFactory

# 使用自己创建的工厂来创建对象，创建的规则是： `别名`.`类名`
Demo = MyFactory.createInstance('demo.Demo')

result_all = Demo.find_all()
result_many = Demo.find_many(sql='SELECT * FROM `demo`')
result_one = Demo.find_one(sql='SELECT * FROM `demo` LIMIT 0,1')
result_field = Demo.find_field('id', 'name', 'password')
result_sql = Demo.find_sql(sql='SELECT * FROM demo')
