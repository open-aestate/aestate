def Table(name, msg, **kwargs):
    """
    标注该类为一个表
    :param name:表的名称
    :param msg:表的描述
    :return:
    """

    def set_to_field(func):
        setattr(func, '__table_name__', name)
        setattr(func, '__table_msg__', msg)
        for key, value in kwargs.items():
            setattr(func, key, value)
        return func

    return set_to_field
