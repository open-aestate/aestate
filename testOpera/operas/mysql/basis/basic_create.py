# -*- utf-8 -*-
# @Time: 2021/7/25 21:36
# @Author: CACode
from testOpera.table.demoModels import TestCreate, Demo

t = TestCreate()
t.orm.create()
Demo().orm.create()
