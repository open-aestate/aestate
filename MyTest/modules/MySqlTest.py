import datetime

from aestate.work.annos import Table, Select
from aestate.work import Manage
from MyTest.modules.DatabaseConf import MySqlConfig


@Table(name='demo_table', msg='')
class DemoTable(Manage.Pojo):
    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField(auto_field=True, primary_key=True)
        self.t_name = Manage.tag.varcharField(default='测试name')
        self.t_msg = Manage.tag.varcharField(default='测试msg')
        self.t_pwd = Manage.tag.varcharField(default='测试pwd')
        self.create_time = Manage.tag.datetimeField(default=datetime.datetime.utcnow(), auto_time=True)
        self.update_time = Manage.tag.datetimeField(default=datetime.datetime.utcnow(), update_auto_time=True)
        super(DemoTable, self).__init__(config_obj=MySqlConfig(), log_conf={
            'path': "/log/",
            'save_flag': True
        }, **kwargs)

    @Select(sql='SELECT * FROM demo_table WHERE t_id<=%s', params=['${t_id}'])
    def find_by_id(self, t_id):
        pass


@Table(name='demo_table', msg='')
class De(Manage.Pojo):
    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField(auto_field=True, primary_key=True)
        self.t_name = Manage.tag.varcharField(default='测试name')
        self.t_msg = Manage.tag.varcharField(default='测试msg')
        self.t_pwd = Manage.tag.varcharField(default='测试pwd')
        self.create_time = Manage.tag.datetimeField(default=datetime.datetime.utcnow(), auto_time=True)
        self.update_time = Manage.tag.datetimeField(default=datetime.datetime.utcnow(), update_auto_time=True)
        super(De, self).__init__(config_obj=MySqlConfig(), log_conf={
            'path': "/log/",
            'save_flag': True
        }, **kwargs)

    @Select(sql='SELECT * FROM demo_table WHERE t_id<=%s', params=['${t_id}'])
    def find_by_id(self, t_id):
        pass
