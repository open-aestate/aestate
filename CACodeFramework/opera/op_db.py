import threading

from CACodeFramework.cacode.Modes import Recursion
from CACodeFramework.cacode.Serialize import JsonUtil
from CACodeFramework.util.Log import CACodeLog

from CACodeFramework.field.MySqlDefault import *
from CACodeFramework.util.ParseUtil import ParseUtil


class DbOperation(object):
    """
    迁移重要操作到此类
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def start(self, *args, **kwargs):
        """
        开始任务
        Attributes:
            func:调用指定的方法
        """
        # 执行的函数体
        func = kwargs['func']
        # 线程独立
        _lock = kwargs['t_local']
        name = kwargs['__task_uuid__']
        log_obj = kwargs['t_local'].log_obj
        if not _lock.close_log:
            CACodeLog.log(obj=kwargs['func'], msg='TASK-{} START'.format(name), task_name=name,
                          LogObject=log_obj)
        # # 设置任务
        # _kw = JsonUtil.load(JsonUtil.parse(_lock))
        _kw = _lock.__dict__
        kwargs.update(_kw)
        _t = threading.Thread(target=func, args=args, kwargs=kwargs, name=name)
        _t.start()
        if not _lock.close_log:
            CACodeLog.log(obj=_t, msg='TASK-{} RUNNING'.format(name), task_name=name, LogObject=kwargs['log_obj'])
        # 等待任务完成
        _t.join()
        # 返回结果
        return self.result

    def __find_all__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12
        任务方法
        """
        return self.__find_by_field__(*args, **kwargs)

    def __find_by_field__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        fields = ParseUtil(*args, is_field=True).parse_key()
        sql_str = kwargs['sqlFields'].find_str + fields + kwargs['sqlFields'].from_str + kwargs['__table_name__']
        kwargs['sql'] = sql_str
        self.result = self.__find_many__(**kwargs)
        return self.result

    def __find_many__(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        # kwargs['conf_obj'] = config_obj
        kwargs = ParseUtil.print_sql(**kwargs)
        self.result = self.__find_sql__(**kwargs)
        return self.result

    def __find_sql__(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        kwargs = ParseUtil.print_sql(**kwargs)
        _rs = kwargs['db_util'].select(**kwargs)

        self.result = []

        for i in _rs:
            self.result.append(ParseUtil.parse_obj(i, kwargs['instance']))

        return self.result

    def __insert_one__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        kwargs = ParseUtil.print_sql(**kwargs)

        kwargs = ParseUtil.last_id(**kwargs)

        if 'pojo' not in kwargs.keys():
            raise SyntaxError('the key of `pojo` cannot be found in the parameters')

        filed_list = ParseUtil.parse_insert_pojo(kwargs['pojo'], __table_name__=kwargs['__table_name__'],
                                                 insert_str=kwargs['sqlFields'].insert_str,
                                                 values_str=kwargs['sqlFields'].values_str)

        kwargs.update(filed_list)

        self.result = kwargs['db_util'].insert(**kwargs)

        return self.result

    def get_result(self):
        """
        获取最后的结果
        """
        return self.result
