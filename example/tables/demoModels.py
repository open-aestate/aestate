# -*- utf-8 -*-
# @Time: 2021/5/25 0:04
# @Author: CACode
from aestate.dbs import _mysql
from example.db_base import table_template
from aestate.work.Annotation import Table


# 使用装示器设置表的名称,name和msg是必填字段,name为表的名称,msg为表的注释
# 如果你不喜欢使用装示器，你也可以在__init__()中使用self.__table_name__来设置表的名称
# 如果你还是不喜欢，那就将这个类的名称写成表的名称，严格区分大小写
# 为了规范起见，请务必填写描述文本
@Table(name='demo', msg='示例表')
# 使用表的全名为类名设置表的名称
# class demo(table_template):
class Demo(table_template):
    def __init__(self, **kwargs):
        # 新建一个名为name的字段，长度为20，不允许为空
        self.name = _mysql.tag.varcharField(length=20, is_null=False, comment='名称')
        # 创建一个password字段
        self.password = _mysql.tag.varcharField(length=20, is_null=False, comment='密码')
        # 使用内部变量设置表的名称
        # self.__table_name__ = 'demo'
        # 这里不设置`is_delete`字段
        super(Demo, self).__init__(**kwargs)


@Table(name='demo_table', msg='示例表')
class DemoTable(table_template):
    def __init__(self, **kwargs):
        self.name = _mysql.tag.varcharField(length=20, is_null=False, comment='名称')
        self.password = _mysql.tag.varcharField(length=20, is_null=False, comment='密码')
        super(DemoTable, self).__init__(**kwargs)


@Table(name='write', msg='写入示例表')
class Write(table_template):
    def __init__(self, **kwargs):
        self.nickname = _mysql.tag.varcharField(length=255, is_null=False, comment='名称')
        self.password = _mysql.tag.varcharField(length=20, is_null=False, comment='密码')
        self.path = _mysql.tag.varcharField(length=255, is_null=False, comment='地址')
        super(Write, self).__init__(**kwargs)


@Table(name='write_cp', msg='示例表')
class WriteCp(table_template):
    def __init__(self, **kwargs):
        self.nickname = _mysql.tag.varcharField(length=255, is_null=False, comment='名称')
        self.password = _mysql.tag.varcharField(length=20, is_null=False, comment='密码')
        self.path = _mysql.tag.varcharField(length=255, is_null=False, comment='地址')
        super(WriteCp, self).__init__(**kwargs)

#
# class TempSchool(BaseModel):
#     create_time = Manage.tag.datetimeField(auto_time=True)
#     update_time = Manage.tag.datetimeField(update_auto_time=True)
#     is_delete = Manage.tag.boolField(default=False)
#
#
# class Student(TempSchool):
#     id = Manage.tag.intField(primary_key=True, auto_field=True)
#     name = Manage.tag.varcharField(length=255)
#     password = Manage.tag.varcharField(length=255)
#
#     class Meta:
#         table_name = "student"
#         description = "学生表"
#
#
# class Teacher(BaseModel):
#     id = Manage.tag.intField(primary_key=True, auto_field=True)
#     name = Manage.tag.varcharField(length=255)
#
#     class Meta:
#         table_name = "teacher"
#         description = "教师表"
#
#
# class STCenter(BaseModel):
#     id = Manage.tag.intField(primary_key=True, auto_field=True)
#     student = Manage.tag.forKey(Student, "id")
#     teacher = Manage.tag.forKey(Teacher, "id")
#
#     class Meta:
#         table_name = "stc"
#         description = "学生和教师的中间表，用于连接学生与教师的多对多关系"
#
#
# class Cls(BaseModel):
#     id = Manage.tag.intField(primary_key=True, auto_field=True)
#     name = Manage.tag.varcharField(length=255)
#
#     class Meta:
#         table_name = "cls"
#         description = "教室表"
#
#
# class CTC(BaseModel):
#     id = Manage.tag.intField(primary_key=True, auto_field=True)
#     cls = Manage.tag.forKey(Cls, "id")
#     teacher = Manage.tag.forKey(Teacher, "id")
#
#     class Meta:
#         table_name = "stc"
#         description = "教室和教师的中间表，用于连接教室与教师的多对多关系"
