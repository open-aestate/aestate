# -*- utf-8 -*-
# @Time: 2021/5/6 17:17
# @Author: CACode
# @File: SqlServerTest.py
# @Software: PyCharm
from summer.anno.annos import Table
from summer.work.Manage import Pojo
from test.modules.DatabaseConf import SqlServerConfig


@Table(name='testccfk', msg='')
class DemoTable(Pojo):
    def __init__(self, **kwargs):
        self.t_id = summer.field.tag.intField()
        self.t_msg = summer.field.tag.intField()
        self.create_time = summer.field.tag.datetimeField()
        super(DemoTable, self).__init__(config_obj=SqlServerConfig(), log_conf={
            'path': "/log/",
            'save_flag': True
        }, **kwargs)
