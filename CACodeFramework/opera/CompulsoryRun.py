class Compulsory(object):
    @staticmethod
    def run_function(func, args, kwargs):
        """
        强制执行
        """
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            pass

        try:
            return func(*args)
        except TypeError as e:
            pass

        try:
            return func(**kwargs)
        except TypeError as e:
            pass

        try:
            return func()
        except TypeError as e:
            pass
