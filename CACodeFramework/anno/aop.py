import types

from CACodeFramework.opera.CompulsoryRun import Compulsory


class AopModelObject(object):
    """
        此类为AopModel提供所有操作
    """

    def __init__(self, before=None, after=None,
                 before_args=None, before_kwargs=None,
                 after_args=None, after_kwargs=None):
        # wraps(func)(self)
        # self.func = func
        # 初始化所有字段
        self.__before_func__ = before
        self.__before_args_data__ = before_args
        self.__before_kwargs_data__ = before_kwargs

        self.__after_func__ = after
        self.__after_args_data__ = after_args
        self.__after_kwargs_data__ = after_kwargs

    def set_func(self, func):
        self.func = func

    def set_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def start(self):
        """
        主操作
        """

        # self.func = args[0]
        self.init_fields()
        # wraps(self.func)(self)
        self.init_attr()

        # 解析参数需要
        # self.before_parse()
        # 执行before操作
        self.before_run()
        # 执行原始数据
        result = self.original_func()
        # after解析
        # self.after_parse(result)
        # after操作
        self.after_run(result)
        # 返回原始数据
        return result

    def init_fields(self):
        # 定义名称规则
        self.after = 'after'
        self.after_args = 'after_args'
        self.after_kwargs = 'after_kwargs'

        self.before = 'before'
        self.before_args = 'before_args'
        self.before_kwargs = 'before_kwargs'

        self.__after__ = '__after_func__'
        self.__after_args__ = '__after_args__'
        self.__after_kwargs__ = '__after_kwargs__'

        # 得到before参数的名称
        self.__before_name__ = self.format_name(self.before)
        self.__before_args_name__ = self.format_name(self.before_args)
        self.__before_kwargs_name__ = self.format_name(self.before_kwargs)

        # 得到after参数的名称

        self.__after_name__ = self.format_name(self.__after__)
        self.__after_args_name__ = self.format_name(self.__after_args__)
        self.__after_kwargs_name__ = self.format_name(self.__after_kwargs__)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def format_name(self, name):
        """
        格式化名称字符串
        """
        return '{}{}'.format(name, self.func.__name__)

    def setters(self, i1, i2, i3, k1, v1, k2, v2, k3, v3):
        """
        批量设置
        """
        if i1 in self.__dict__.keys():
            setattr(self, v1, self.__dict__[k1])
            if i2 in self.__dict__.keys():
                setattr(self, v2, self.__dict__[k2])
            if i3 in self.__dict__.keys():
                setattr(self, v3, self.__dict__[k3])

    def init_attr(self):
        """
        初始化cls下的字段
        通过使用setters下的setter()功能批量解析是否需要before或者after操作
        """

        self.setters(
            i1=self.before,
            i2=self.before_args,
            i3=self.before_kwargs,
            k1=self.before,
            k2=self.before_args,
            k3=self.before_kwargs,
            v3=self.__before_kwargs_name__,
            v1=self.__before_name__,
            v2=self.__before_args_name__,
        )

        self.setters(
            i1=self.after,
            i2=self.after_args,
            i3=self.after_kwargs,
            k1=self.after,
            k2=self.after_args,
            k3=self.after_kwargs,
            v1=self.__after_name__,
            v2=self.__after_args_name__,
            v3=self.__after_kwargs_name__
        )

    # def before_parse(self):
    #     """
    #     解析before参数的方法需要什么参数类型
    #     """
    #     __before_func__ = None
    #     __before_args_data__ = None
    #     __before_kwargs_data__ = None
    #     # 如果包含切入函数的字段
    #     if hasattr(self, self.__before_name__):
    #         # 得到参数的名称
    #         __before_func__ = getattr(self, self.__before_name__)
    #         if hasattr(self, self.__before_args_name__) and hasattr(self, self.__before_kwargs_name__):
    #
    #             __before_args_data__ = getattr(self, self.__before_args_name__)
    #             __before_kwargs_data__ = getattr(self, self.__before_kwargs_name__)
    #
    #         elif hasattr(self, self.__before_args_name__):
    #             __before_args_data__ = getattr(self, self.__before_args_name__)
    #
    #         elif hasattr(self, self.__before_kwargs_name__):
    #             __before_kwargs_data__ = getattr(self, self.__before_kwargs_name__)
    #
    #     # 批添加方法、参数和键值对
    #     self.__before_func__ = __before_func__
    #     self.__before_args_data__ = __before_args_data__
    #     self.__before_kwargs_data__ = __before_kwargs_data__

    def before_run(self):
        """
        执行before方法
        """
        if self.__before_func__ and self.__before_args_data__ and self.__before_kwargs_data__:
            self.__before_func__(*self.__before_args_data__, **self.__before_kwargs_data__)
        elif self.__before_func__ and self.__before_args_data__:
            self.__before_func__(*self.__before_args_data__)
        elif self.__before_func__ and self.__before_kwargs_data__:
            self.__before_func__(**self.__before_kwargs_data__)
        elif self.__before_func__:
            self.__before_func__()
        else:
            pass

    # def after_parse(self, result):
    #     """
    #     解析追加方法
    #     :param result:原始方法返回的值
    #     """
    #     __after_func__ = None
    #     __after_args_data__ = None
    #     __after_kwargs_data__ = {}
    #     # 如果包含切入函数的字段
    #     if hasattr(self, self.__after_name__):
    #         # 得到参数的名称
    #         __after_func__ = getattr(self, self.__after_name__)
    #         if hasattr(self, self.__after_args_name__) and hasattr(self, self.__after_kwargs_name__):
    #
    #             __after_args_data__ = getattr(self, self.__after_args_name__)
    #             __after_kwargs_data__ = getattr(self, self.__after_kwargs_name__)
    #
    #         elif hasattr(self, self.__after_args_name__):
    #             __after_args_data__ = getattr(self, self.__after_args_name__)
    #
    #         elif hasattr(self, self.__after_kwargs_name__):
    #             __after_kwargs_data__ = getattr(self, self.__after_kwargs_name__)
    #
    #     # 批添加方法、参数和键值对
    #     self.__after_func__ = __after_func__
    #     self.__after_args_data__ = __after_args_data__
    #     __after_kwargs_data__.update({'result': result})
    #     self.__after_kwargs_data__ = __after_kwargs_data__

    def after_run(self, result):
        """
        执行after方法
        """
        if self.__after_kwargs_data__ is None:
            self.__after_kwargs_data__ = {}

            self.__after_kwargs_data__.update({'result': result})
        if self.__after_func__ and self.__after_args_data__ and self.__after_kwargs_data__:
            self.__after_func__(*self.__after_args_data__, **self.__after_kwargs_data__)
        elif self.__after_func__ and self.__after_args_data__:
            self.__after_func__(*self.__after_args_data__)
        elif self.__after_func__ and self.__after_kwargs_data__:
            self.__after_func__(**self.__after_kwargs_data__)
        elif self.__after_func__:
            self.__after_func__()
        else:
            pass

    def original_func(self):
        """
        最后耍无赖方法返回函数执行的结果
        使用四个try逐一抛出
        """
        return Compulsory.run_function(func=self.func, args=self.args, kwargs=self.kwargs)
        # try:
        #     return self.func(*self.args, **self.kwargs)
        # except TypeError as e:
        #     pass
        #
        # try:
        #     return self.func(*self.args)
        # except TypeError as e:
        #     pass
        #
        # try:
        #     return self.func(**self.kwargs)
        # except TypeError as e:
        #     pass
        #
        # try:
        #     return self.func()
        # except TypeError as e:
        #     pass
