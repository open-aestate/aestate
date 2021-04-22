import types
from functools import wraps


def Table(name, msg, **kwargs):
    """
    标注该类为一个表
    :param name:表的名称
    :param msg:表的描述
    :return:
    """

    def set_to_field(cls):
        setattr(cls, '__table_name__', name)
        setattr(cls, '__table_msg__', msg)
        for key, value in kwargs.items():
            setattr(cls, key, value)
        return cls

    return set_to_field


def Select(sql, params=None, print_sql=False):
    def base_func(cls):
        def _wrapper_(*args, **kwargs):
            l = list(args)
            del l[0]
            cls_obj = cls(*l, **kwargs)
            obj = cls_obj.meta()

            result = obj.find_sql(sql=sql, params=params, print_sql=print_sql)
            setattr(cls_obj, 'result', result)

            return cls_obj

        return _wrapper_

    return base_func
