# -*- utf-8 -*-
# @Time: 2021/5/25 0:33
# @Author: CACode
from example.db_base import MyFactory

# 使用自己创建的工厂来创建对象，创建的规则是： `别名`.`类名`
Demo = MyFactory.createInstance('demo.Demo')
result = Demo.orm.find().order_by('id').end()
page = result.page(10).get(0)

# 查找所有
result_all = Demo.find_all()
print('result_all', result_all)
# 搜索多个
result_many = Demo.find_many(sql='SELECT * FROM `demo`')
print('result_many', result_many)
# 搜索一个
result_one = Demo.find_one(sql='SELECT * FROM `demo` WHERE `id`=1')
print('result_one', result_one.to_json())
# 根据字段查找多个
result_field = Demo.find_field('id', 'name', 'password')
print('result_field', result_field)
# 根据sql查找
result_sql = Demo.find_sql(sql='SELECT * FROM demo')
print('result_sql', result_sql)
