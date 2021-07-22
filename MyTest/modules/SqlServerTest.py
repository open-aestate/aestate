# -*- utf-8 -*-
# @Time: 2021/5/6 17:17
# @Author: CACode
# @File: SqlServerTest.py
# @Software: PyCharm
from aestate.work.Annotation import Table
from aestate.work import Manage
from MyTest.modules.DatabaseConf import SqlServerConfig


@Table(name='testccfk', msg='')
class DemoTable(Manage.Pojo):
    def __init__(self, **kwargs):
        self.t_id = aestate.dbs._mysql.tag.intField()
        self.t_msg = aestate.dbs._mysql.tag.intField()
        self.create_time = aestate.dbs._mysql.tag.datetimeField()
        super(DemoTable, self).__init__(config_obj=SqlServerConfig(), log_conf={
            'path': "/log/",
            'save_flag': True
        }, **kwargs)
