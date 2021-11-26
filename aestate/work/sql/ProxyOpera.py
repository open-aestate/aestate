from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor()


class DbOperation(object):
    """
    迁移重要操作到此类
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

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
        # # 设置任务
        # _kw = aj.load(aj.parse(_lock))
        _kw = _lock.__dict__
        kwargs.update(_kw)
        _t = pool.submit(lambda x, y: func(*x, **y), args, kwargs)
        # _t = threading.Thread(target=func, args=args, kwargs=kwargs, name=name)
        # if not _lock.close_log:
        #     ALog.log(obj=_t, msg='RUNNING', task_name=name, LogObject=log_obj)
        result = _t.result()
        # 返回结果
        return result[name]

    def __find_all__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12
        任务方法
        """
        return self.__find_by_field__(*args, **kwargs)

    def __find_by_field__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        fields = kwargs['config_obj'].parse_key(*args, is_field=True, left=kwargs['sqlFields'].left_subscript,
                                                right=kwargs['sqlFields'].right_subscript)
        sql_str = kwargs['sqlFields'].find_str + fields + kwargs['sqlFields'].from_str + kwargs['__table_name__']
        kwargs['sql'] = sql_str
        return self.__find_many__(**kwargs)

    def __find_many__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        # kwargs['conf_obj'] = config_obj
        # kwargs = kwargs['ParseUtil'].find_print_sql(**kwargs)
        return self.__find_sql__(**kwargs)

    def __find_sql__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        任务方法
        """
        kwargs = kwargs['ParseUtil'].find_print_sql(**kwargs)
        _rs = kwargs['db_util'].select(**kwargs)

        result = []

        for i in _rs:
            result.append(kwargs['ParseUtil'].parse_obj(i, kwargs['instance']))

        return {
            kwargs['__task_uuid__']: result
        }

    def __insert__(self, *args, **kwargs):
        """作者:CACode 最后编辑于2021/4/12
        :param pojo: pojo对象
        任务方法
        """
        kwargs = kwargs['ParseUtil'].find_print_sql(**kwargs)

        kwargs = kwargs['ParseUtil'].find_last_id(**kwargs)
        kwargs['ParseUtil'].fieldExist(kwargs, 'pojo', raise_exception=True)

        if 'many' in kwargs and kwargs['many']:
            # 多行插入 这个先取出sql语句,params无作用
            for item in kwargs['pojo']:
                filed_list = kwargs['config_obj'].parse_insert_pojo(item,
                                                                    __table_name__=kwargs['__table_name__'],
                                                                    insert_str=kwargs['sqlFields'].insert_str,
                                                                    values_str=kwargs['sqlFields'].values_str)

                if 'params' not in kwargs.keys() or not isinstance(kwargs['params'], list):
                    kwargs['params'] = []
                kwargs['sql'] = filed_list['sql']
                kwargs['params'].append(filed_list['params'])

        else:
            filed_list = kwargs['config_obj'].parse_insert_pojo(kwargs['pojo'], __table_name__=kwargs['__table_name__'],
                                                                insert_str=kwargs['sqlFields'].insert_str,
                                                                values_str=kwargs['sqlFields'].values_str)

            kwargs.update(filed_list)
        return {
            kwargs['__task_uuid__']: kwargs['db_util'].insert(**kwargs)
        }

    def __update__(self, *args, **kwargs):
        kwargs = kwargs['ParseUtil'].find_print_sql(**kwargs)

        kwargs = kwargs['ParseUtil'].find_last_id(**kwargs)
        kwargs['sql'], kwargs['params'] = kwargs['config_obj'].parse_update(kwargs['pojo'], kwargs['key'])

        return {
            kwargs['__task_uuid__']: kwargs['db_util'].update(**kwargs)
        }

    def __remove__(self, *args, **kwargs):
        kwargs = kwargs['ParseUtil'].find_print_sql(**kwargs)

        kwargs = kwargs['ParseUtil'].find_last_id(**kwargs)
        kwargs['sql'], kwargs['params'] = kwargs['config_obj'].parse_remove(kwargs['pojo'], kwargs['key'])

        return {
            kwargs['__task_uuid__']: kwargs['db_util'].update(**kwargs)
        }
