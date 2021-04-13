import copy
import sys
import threading

from CACodeFramework.MainWork.exception import e_fields, e_except
from CACodeFramework.field.sql_fields import *
from CACodeFramework.util.ParseUtil import ParseUtil

_result = None


class parses(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def log(self, _obj, msg, name='\t\tTask', LogObject=None):
        """
        输出任务执行日志

        :param _obj:任务对象的值

        """
        # 获得该函数被调用前的行号
        _l = sys._getframe().f_back.f_lineno
        # 格式：时间 类型 日志名称 对象地址 被调用行号 执行类型 信息
        info = e_except.warn(obj=_obj, line=_l, task_name=name, f_warn=e_fields.INFO, msg=msg, LogObject=LogObject)

    def last_id(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        遵循规则：

            内部>配置文件

        是否包含返回最后一行ID的配置

        只存在于更新操做的方法内，如：

            insert,

            update,

            delete

         Attributes:

             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'last_id' not in kwargs.keys():
            if 'last_id' in conf_obj.conf.keys():
                kwargs['last_id'] = conf_obj.conf['last_id']
            else:
                kwargs['last_id'] = False
        return kwargs

    def print_sql(self, **kwargs):
        """
        遵循规则：
            内部>配置文件

        是否包含打印sql的配置

        存在于所有数据库操做

        Attributes:
             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'print_sql' not in kwargs.keys():
            if 'print_sql' in conf_obj.conf.keys():
                kwargs['print_sql'] = conf_obj.conf['print_sql']
            else:
                kwargs['print_sql'] = False
        return kwargs

    def parse_insert(self, pojo, __table_name__):
        """
        解析插入语句
        :param pojo:POJO对象
        :param __table_name__:表名
        :return:
        """
        _dict = pojo.__dict__
        keys = []
        values = []
        for key, value in _dict.items():
            if value is None:
                continue
            keys.append(key)
            values.append(value)
        return ParseUtil().parse_insert(keys, values, __table_name__)

    def parse_obj(self, data: dict, participants):
        """
        将数据解析成对象
        注意事项:
            数据来源必须是DbUtil下查询出来的
        :param data:单行数据
        :param participants:参与解析的对象
        :return:POJO对象
        """
        # 深度复制对象
        part_obj = copy.copy(participants)
        for key, value in data.items():
            setattr(part_obj, key, value)
        return part_obj

    def get_result(self):
        """作者:CACode 最后编辑于2021/4/12

        获取返回结果

        Return:
            执行返回结果

        """
        # global _result
        return _result


class DbOperation(object):
    """
    迁移重要操作到此类
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.parse_util = parses()

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
        name = kwargs['__table_name__']
        if not _lock.close_log:
            self.parse_util.log(_obj=kwargs['func'], msg='TASK-{} START'.format(name), name=name)
        # # 设置任务
        # _kw = JsonUtil.load(JsonUtil.parse(_lock))
        _kw = _lock.__dict__
        kwargs.update(_kw)
        _t = threading.Thread(target=func, args=args, kwargs=kwargs, name=name)
        _t.start()
        if not _lock.close_log:
            self.parse_util.log(_obj=_t, msg='TASK-{} RUNNING'.format(name), name=name)
        # 等待任务完成
        _t.join()
        # 返回结果

    def __find_all__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12
        任务方法
        """
        return self.__find_by_field__(*args, **kwargs)

    def __find_by_field__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        global _result
        fields = ParseUtil(*args, is_field=True).parse_key()
        sql_str = find_str + fields + from_str + kwargs['table_name']
        kwargs['sql'] = sql_str
        _result = self.__find_many__(**kwargs)
        return _result

    def __find_many__(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        config_obj = kwargs['config_obj']
        kwargs['conf_obj'] = config_obj
        kwargs = self.parse_util.print_sql(**kwargs)
        _r = self.__find_sql__(**kwargs)
        _pojo_list = []
        for item in _r:
            pojo = self.parse_util.parse_obj(item, participants=kwargs['participants'])
            _pojo_list.append(pojo)
        return _pojo_list

    def __find_sql__(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        global _result
        kwargs = self.parse_util.print_sql(**kwargs)
        _result = kwargs['db_util'].select(**kwargs)
        return _result

    def __insert_one__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        global _result
        kwargs = self.parse_util.print_sql(**kwargs)
        kwargs = self.parse_util.last_id(**kwargs)
        if 'pojo' not in kwargs.keys():
            raise SyntaxError('the key of `pojo` cannot be found in the parameters')
        _result = self.parse_util.parse_insert(kwargs['pojo'], __table_name__=kwargs['table_name'])
        kwargs['sql'] = _result['sql']
        kwargs['params'] = _result['params']
        _result = kwargs['db_util'].insert(**kwargs)
        return _result
