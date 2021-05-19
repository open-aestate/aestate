# -*- utf-8 -*-
# @Time: 2021/5/6 17:17
# @Author: CACode
# @File: SqlServerTest.py
# @Software: PyCharm
from cacode_framework.anno.annos import Table
from cacode_framework.pojoManager import Manage
from cacode_framework.pojoManager.Manage import Pojo
from test.modules.DatabaseConf import SqlServerConfig


@Table(name='testccfk', msg='')
class DemoTable(Pojo):
    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField()
        self.t_msg = Manage.tag.intField()
        self.create_time = Manage.tag.datetimeField()
        super(DemoTable, self).__init__(config_obj=SqlServerConfig(), log_conf={
            'path': "/log/",
            'save_flag': True
        }, **kwargs)
