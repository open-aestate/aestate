from aestate.dbs._mysql import tag
from db_base import table_template
from aestate.work.Annotation import Table, Select, SelectAbst, ReadXml, Item, AopModel


def Before():
    print("before")


def After(result):
    print('result', result)


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
        self.name = tag.varcharField(length=20, is_null=False, comment='名称')
        # 创建一个password字段
        self.password = tag.varcharField(
            length=20, is_null=False, comment='密码')
        # 使用内部变量设置表的名称
        # self.__table_name__ = 'demo'
        # 这里不设置`is_delete`字段
        super(Demo, self).__init__(**kwargs)

    @AopModel(before=Before, after=After)
    @Select("SELECT * FROM demo WHERE id=${id} AND name=#{name}")
    def find_all_where_id(self, id, name): ...

    @SelectAbst()
    def find_all_F_where_id_eq_and_name_eq(self, **kwargs): ...

    @SelectAbst()
    def find_all_F_where_id_in_and_name_like_order_by_id(
        self, **kwargs) -> list: ...

    @AopModel(before=Before, after=After)
    @SelectAbst()
    def find_all_F(self, **kwargs): ...


@ReadXml("./test.xml")
@Table(name='demo', msg='示例表')
class ReadXmlClass(table_template):
    """读取xml"""

    @Item(_id="findInDemo")
    def findInDemo(self, **kwargs): ...

    @Item(_id="findAllById")
    def findAllById(self, **kwargs): ...

    @Item(_id="findAllById", d=True)
    def findAllByIdDict(self, **kwargs): ...

    @Item(_id="insertTest")
    def insertTest(self, **kwargs): ...

    @Item(_id="updateTest")
    def updateTest(self, **kwargs): ...

    @Item(_id="deleteTest")
    def deleteTest(self, **kwargs): ...


@Table(name='test_create', msg='测试创建表')
class TestCreate(table_template):
    def __init__(self, **kwargs):
        self.name = tag.varcharField(length=20, is_null=False, comment='名称')
        super(TestCreate, self).__init__(**kwargs)
