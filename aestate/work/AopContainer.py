import types

from aestate.util.CompulsoryRun import Compulsory


class AopModelObject(object):
    """
        此类为AopModel提供所有操作
    """

    def __init__(self, before=None, after=None,
                 before_args=None, before_kwargs=None,
                 after_args=None, after_kwargs=None):
        # 初始化所有字段
        self.__before_func__ = before
        self.__before_args_data__ = before_args
        self.__before_kwargs_data__ = before_kwargs

        self.__after_func__ = after
        self.__after_args_data__ = after_args
        self.__after_kwargs_data__ = after_kwargs

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
        result = Compulsory.run_function(
            func=self.func, args=self.args, kwargs=self.kwargs)
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

    def before_run(self):
        """
        执行before方法
        """
        if self.__before_func__ and self.__before_args_data__ and self.__before_kwargs_data__:
            self.__before_func__(*self.__before_args_data__,
                                 **self.__before_kwargs_data__)
        elif self.__before_func__ and self.__before_args_data__:
            self.__before_func__(*self.__before_args_data__)
        elif self.__before_func__ and self.__before_kwargs_data__:
            self.__before_func__(**self.__before_kwargs_data__)
        elif self.__before_func__:
            self.__before_func__()
        else:
            pass

    def after_run(self, result):
        """
        执行after方法
        """
        if self.__after_kwargs_data__ is None:
            self.__after_kwargs_data__ = {}

            self.__after_kwargs_data__.update({'result': result})
        if self.__after_func__ and self.__after_args_data__ and self.__after_kwargs_data__:
            self.__after_func__(*self.__after_args_data__,
                                **self.__after_kwargs_data__)
        elif self.__after_func__ and self.__after_args_data__:
            self.__after_func__(*self.__after_args_data__)
        elif self.__after_func__ and self.__after_kwargs_data__:
            self.__after_func__(**self.__after_kwargs_data__)
        elif self.__after_func__:
            self.__after_func__()
        else:
            pass
