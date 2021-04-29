from CACodeFramework.anno.annos import Select, Table, AopModel
from CACodeFramework.pojoManager import Manage
from CACodeFramework.util.Log import CACodeLog
from test.modules.DatabaseConf import ConF


def Before(**kwargs):
    print('Before:', kwargs)


def After(*args, **kwargs):
    print('After', args)
    print('Result:', kwargs)


@Table(name='demo_table', msg='测试类')
class DemoTable(Manage.Pojo):

    def __init__(self, **kwargs):
        self.t_id = Manage.tag.intField(primary_key=True)
        self.t_name = Manage.tag.varcharField(length=255)
        self.t_pwd = Manage.tag.varcharField(length=255)
        self.t_msg = Manage.tag.varcharField(length=255)
        self.create_time = Manage.tag.datetimeField(auto_time=True)
        self.update_time = Manage.tag.datetimeField(update_auto_time=True)

        super(DemoTable, self).__init__(config_obj=ConF(), log_conf={
            'path': "/log",
            'save_flag': True
        }, **kwargs)

    @AopModel(before=Before, before_kwargs={'1': '1'}, after=After)
    def find_title_and_selects(self, **kwargs):
        print('function task', kwargs['uid'])
        _r = self.orm.find().end()
        print(_r)
        return _r

    @Select(sql="SELECT * FROM demo_table WHERE t_id<=%s AND t_msg like %s",
            params=['10', '%${t_id}${t_msg}%'])
    class FindWheresTIdAndTMsg:
        def __init__(self, t_id, t_msg):
            self.meta = DemoTable

    @Select(sql="SELECT * FROM demo_table WHERE t_id<=%s ORDER BY t_id DESC",
            params=['${t_id}'])
    def FindAllWhereTID(self, t_id):
        pass


if __name__ == '__main__':
    DemoTable().save()