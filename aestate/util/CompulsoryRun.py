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

        return None

    @staticmethod
    def search_target(module, target_names):

        """
        深度搜素树
        """

        from aestate.util.Log import ALog

        if len(target_names) == 0:
            return module
        # 当前的标记位置
        now_target = target_names[0]
        del target_names[0]
        if hasattr(module, now_target):
            next_module = getattr(module, now_target)
            return Compulsory.search_target(next_module, target_names)
        else:
            ALog.log_error(f'The package name does not exist in the search tree: {now_target}, please check ' +
                           'whether the package name is filled in correctly', ImportError, raise_exception=True)
