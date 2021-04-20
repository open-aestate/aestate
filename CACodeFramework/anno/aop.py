import types
from functools import wraps


class AopModel:
    """AOP面向切面编程

            面向切面的程序设计将代码逻辑切分为不同的模块（即关注点（Concern），一段特定的逻辑功能)。几乎所有的编程思想都涉及代码功能的分类，

        将各个关注点封装成独立的抽象模块（如函数、过程、模块、类以及方法等），后者又可供进一步实现、封装和重写。部分关注点“横切”程序代码中的数个模块，

        即在多个模块中都有出现，它们即被称作横切关注点（Cross-cutting concerns, Horizontal concerns）。



        Attributes:

             before:切入时需要执行的函数

             after:切出前需要执行的参数

             before_args:切入的参数
                传入的列表或元组类型数据
                如果是需要使用当前pojo中的内容时，传参格式为:(pojo.字段名)
                可扩展格式，例如需要传入字典

             before_kwargs:切入的参数 -- 传入的字典数据

             after_args:切出的参数
                传入的列表或元组类型数据
                如果是需要使用当前pojo中的内容时，传参格式为:('self.字段名')
                可扩展格式，例如需要传入字典:('self.dict.key')

             after_kwargs:切出的参数 -- 传入的字典数据


        """

    def __init__(self, func, before=None, after=None, before_args=None, before_kwargs=None, after_args=None,
                 after_kwargs=None):
        wraps(func)(self)
        self.func = func

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

    def __call__(self, *args, **kwargs):
        """
        主操作
        """
        # 初始化attr字段参数
        self.init_attr(*args, **kwargs)
        # 解析参数需要
        self.before_parse()
        # 执行before操作
        self.before_run()
        # 执行原始数据
        result = self.original_func()
        # after解析
        self.after_parse()
        # after操作
        self.after_run()
        # 返回原始数据
        return result

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
        if i1 in self.kwargs.keys():
            setattr(self.cls, v1, self.kwargs[k1])
            if i2 in self.kwargs.keys():
                setattr(self.cls, v2, self.kwargs[k2])
            if i3 in self.kwargs.keys():
                setattr(self.cls, v3, self.kwargs[k3])

    def init_attr(self, *args, **kwargs):
        """
        初始化cls下的字段
        通过使用setters下的setter()功能批量解析是否需要before或者after操作
        """

        # 将这参数移送到全局
        self.args = args
        # 这是方法前面的self参数。表示为该方法所对应的字段
        self.cls = args[0]
        self.kwargs = kwargs

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

    def before_parse(self):
        """
        解析before参数的方法需要什么参数类型
        """
        __before_func__ = None
        __before_args_data__ = None
        __before_kwargs_data__ = None
        # 如果包含切入函数的字段
        if hasattr(self.cls, self.__before_name__):
            # 得到参数的名称
            __before_func__ = getattr(self.cls, self.__before_name__)
            if hasattr(self.cls, self.__before_args_name__) and hasattr(self.cls, self.__before_kwargs_name__):

                __before_args_data__ = getattr(self.cls, self.__before_args_name__)
                __before_kwargs_data__ = getattr(self.cls, self.__before_kwargs_name__)

            elif hasattr(self.cls, self.__before_args_name__):
                __before_args_data__ = getattr(self.cls, self.__before_args_name__)

            elif hasattr(self.cls, self.__before_kwargs_name__):
                __before_kwargs_data__ = getattr(self.cls, self.__before_kwargs_name__)

        # 批添加方法、参数和键值对
        self.__before_func__ = __before_func__
        self.__before_args_data__ = __before_args_data__
        self.__before_kwargs_data__ = __before_kwargs_data__

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

    def after_parse(self):
        """
        解析追加方法
        """
        __after_func__ = None
        __after_args_data__ = None
        __after_kwargs_data__ = None
        # 如果包含切入函数的字段
        if hasattr(self.cls, self.__after_name__):
            # 得到参数的名称
            __after_func__ = getattr(self.cls, self.__after_name__)
            if hasattr(self.cls, self.__after_args_name__) and hasattr(self.cls, self.__after_kwargs_name__):

                __after_args_data__ = getattr(self.cls, self.__after_args_name__)
                __after_kwargs_data__ = getattr(self.cls, self.__after_kwargs_name__)

            elif hasattr(self.cls, self.__after_args_name__):
                __after_args_data__ = getattr(self.cls, self.__after_args_name__)

            elif hasattr(self.cls, self.__after_kwargs_name__):
                __after_kwargs_data__ = getattr(self.cls, self.__after_kwargs_name__)

        # 批添加方法、参数和键值对
        self.__after_func__ = __after_func__
        self.__after_args_data__ = __after_args_data__
        self.__after_kwargs_data__ = __after_kwargs_data__

    def after_run(self):
        """
        执行after方法
        """
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
        try:
            return self.__wrapped__(*self.args, **self.kwargs)
        except TypeError as e:
            pass

        try:
            return self.__wrapped__(*self.args)
        except TypeError as e:
            pass

        try:
            return self.__wrapped__(**self.kwargs)
        except TypeError as e:
            pass

        try:
            return self.__wrapped__()
        except TypeError as e:
            pass
