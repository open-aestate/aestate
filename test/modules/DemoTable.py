from CACodeFramework.anno.annos import Table
from CACodeFramework.pojoManager import Manage
from CACodeFramework.pojoManager.Manage import Pojo
from test.modules.DatabaseConf import DemoConF


@Table(name='demo_table', msg='')
class DemoTable(Pojo):
    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField()
        self.t_name = Manage.tag.intField()
        self.t_msg = Manage.tag.intField()
        self.t_pwd = Manage.tag.intField()
        self.create_time = Manage.tag.datetimeField()
        self.update_time = Manage.tag.datetimeField()
        super(DemoTable, self).__init__(config_obj=DemoConF(), log_conf={
            'path': "/log/",
            'save_flag': True
        }, **kwargs)
