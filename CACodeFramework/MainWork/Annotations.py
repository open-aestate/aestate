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


def Operations():
    """
    标注该类为一个操做
    :return:
    """

    def set_to_field(func):
        print('1111111')
        return func

    return set_to_field


def Before(function):
    """
    切入操做，在执行函数之前切入指定函数

    切入:

        在执行函数之前首先执行指定操做称为切入

    """

    def set_to_field(func):
        print('1111111')
        return func

    return set_to_field


def After(function):
    """
    切出操做，在执行函数之前切出指定函数

    切出:

        在指定函数调用完毕时执行得操做成为切除
    """

    def set_to_field(func):
        print('1111111')
        return func

    return set_to_field


from functools import wraps


def decorater(func):
    @wraps(func)  # 保持原函数名不变
    def wrapper(*args, **kwargs):
        print('位置参数:{}'.format(args))
        print('关键字参数:{}'.format(kwargs))
        res = func(*args, **kwargs)
        print('装饰器内函数名:%s' % func.__name__)
        print('返回值:%s' % res)
        print('函数func所属的类:%s' % func.__qualname__)
        print('被调用时的行号:', sys._getframe().f_back.f_lineno)
        return res

    return wrapper


class Name():
    @decorater
    def func2(self, *args, **kwargs):
        return 'return'


if __name__ == '__main__':
    a = Name()
    a.func2(1, 2, a=3, b=4)
    print('装饰外内函数名:%s' % a.func2.__name__)
