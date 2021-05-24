# -*- utf-8 -*-
# @Time: 2021/5/25 0:04
# @Author: CACode
from example.db_base import table_template
from summer.anno.annos import Table
from summer.work import Manage


# 使用装示器设置表的名称,name和msg是必填字段,name为表的名称,msg为表的注释
# 如果你不喜欢使用装示器，你也可以在__init__()中使用self.__table_name__来设置表的名称
# 如果你还是不喜欢，那就将这个类的名称写成表的名称，严格区分大小写
@Table(name='demo', msg='示例表')
class Demo(table_template):
    def __init__(self, **kwargs):
        # 新建一个名为name的字段，长度为20，不允许为空
        self.name = Manage.tag.varcharField(length=20, is_null=False, comment='名称')
        # 创建一个password字段
        self.password = Manage.tag.varcharField(length=20, is_null=False, comment='密码')
        # 这里不设置`is_delete`字段

        self.__table_name__ = 'demo'
        super(Demo, self).__init__(**kwargs)
