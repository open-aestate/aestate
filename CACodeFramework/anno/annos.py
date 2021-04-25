import re


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


def parse_kwargs(params, pattern, kwargs):
    """
    通过${key}方式解析特殊字段
    """
    new_args = []
    for i in params:
        context = re.match(pattern, str(i))
        if context:
            key = str(context.string).replace('${', '').replace('}', '')
            new_args.append(kwargs[key])
        else:
            new_args.append(i)
    return new_args


def Select(sql, params=None, print_sql=False, first=False):
    def base_func(cls):
        def _wrapper_(*args, **kwargs):
            l = list(args)
            del l[0]
            cls_obj = cls(*l, **kwargs)
            obj = cls_obj.meta()

            new_args = parse_kwargs(params, r'^\${.*}$', kwargs)

            result = obj.find_sql(sql=sql, params=new_args, print_sql=print_sql)
            # setattr(cls_obj, 'result', result)
            if first:
                if type(result) is list and len(result) != 0:
                    result = result[0]

            return result

        return _wrapper_

    return base_func
