# -*- utf-8 -*-
# @Time: 2021/5/24 23:34
# @Author: CACode
import pymysql

from aestate.work.Config import Conf
from aestate.cacode.Factory import Factory
from aestate.work import Manage


class db_conf(Conf):
    def __init__(self):
        # 设置全局打印sql语句
        self.set_field('print_sql', True)
        # 设置全局插入语句返回最后一行id
        self.set_field('last_id', True)

        super(db_conf, self).__init__(
            # 数据库地址
            host='localhost',
            # 数据库端口
            port=3306,
            # 数据库名
            database='summer-demo',
            # 数据库用户
            user='root',
            # 数据库密码
            password='123456',
            # 数据库创建者，如果你用的是mysql，那么这里就是pymysql，如果用的是sqlserver，那么这里就应该是pymssql
            creator=pymysql)


class table_template(Manage.Pojo):
    def __init__(self, **kwargs):
        """
        模板类对象
        """
        # 创建一个自增的主键id，并且不允许为空
        self.id = Manage.tag.intField(primary_key=True, is_null=False, comment='主键自增')
        # 创建一个创建时间，并设置`auto_time=True`，在第一次保存时可以为其设置默认为当前时间
        self.create_time = Manage.tag.datetimeField(auto_time=True, is_null=False, comment='创建时间')
        # 创建一个更新时间，并设置`update_auto_time=True`，保证每次修改都会更新为当前时间
        self.update_time = Manage.tag.datetimeField(update_auto_time=True, is_null=False, comment='更新实际按')
        # 如果子类包含`is_delete`字段，并且不为False时，为其添加一个是否删除的字段
        if 'is_delete' in kwargs.keys() and kwargs.get('is_delete'):
            # 设置是否删除，推荐使用int(boolean)
            self.is_delete = Manage.tag.tinyintField(default=int(False), is_null=False, comment='是否删除，0 未删除 1 删除')
        # 设置config_obj未db_conf的对象，
        super(table_template, self).__init__(
            # 导入配置类
            config_obj=db_conf(),
            # 设置日志配置
            log_conf={
                # 保存位置
                'path': "/log/",
                # 是否允许保存日志
                'save_flag': True,
                # 当日志到达多少MB时删除日志重新记录
                'max_clear': 100
            },
            # 必备的字段，每一个Pojo对象都必须包含一个`**kwargs`
            **kwargs)


class MyFactory(Factory):
    # 这个是固定不变的，务必要死记下来
    modules = {
        # 设置映射关系为 `别名`:`包的位置`
        'demo': 'example.tables.demoModels'
    }
