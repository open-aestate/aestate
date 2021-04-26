import copy
import threading
from CACodeFramework.exception import e_fields
from CACodeFramework.opera.CompulsoryRun import Compulsory
from CACodeFramework.util.Log import CACodeLog
import importlib


class Factory(object):

    def __init__(self):
        if not hasattr(self, 'instances'):
            CACodeLog.err(SyntaxError, e_fields.CACode_Factory_Error(
                'Please import the Pojo module first,请先设置导入pojo模块'))
        else:
            self.instances = self.instances

        self.modules = {}
        self.lo = threading.RLock()

        self.__base_init__()

    def __base_init__(self):
        for package_name in self.instances:
            base_module = str(package_name).split('.')
            last_name = base_module[
                (len(base_module) - 1) if
                len(base_module) > 0 else
                CACodeLog.err(TypeError,
                              e_fields.CACode_Factory_Error(
                                  '找不到模块，也许是未设置instances')
                              )
            ]
            # 将包导入
            self.modules[last_name] = package_name

    def createInstance(self, name: str, args=None, kwargs=None):
        """
        建造一个对象并将对象实例化

        使用方法:

        class MyFactory(Factory):
            def __init__(self):
                self.instances = [
                    'test.modules.Demo',
                    'test.modules.BaseData',
                ]
                super().__init__()


        if __name__ == '__main__':
            myFactory = MyFactory()
            ins = myFactory.createInstance("Demo.DemoTable",kwargs={})
            print(ins)




        :param name:类的名称,从配置的instances开始获得
        :param args:类的名称,从配置的instances开始获得
        :param kwargs:类的名称,从配置的instances开始获得
        """
        module_names = str(name).split('.')
        first_module = module_names[0]
        del module_names[0]

        assert len(module_names) > 0

        import_module = importlib.import_module(self.modules[first_module])

        # import_module = __import__(self.modules[first_module])

        # all_modules = getattr(import_module, first_module)
        result = self.search_target(import_module, module_names)

        end_obj = Compulsory.run_function(func=result, args=args, kwargs=kwargs)

        return end_obj

    def __get__(self, instance, owner):
        if not hasattr(self, 'lo'):
            with instance.lo.lock():
                lock = instance.__new__()
            return instance
        else:
            self.instances = instance
            return self.instances

    def search_target(self, module, target_names):
        if len(target_names) == 0:
            return module
        # 当前的标记位置
        now_target = target_names[0]
        del target_names[0]
        if hasattr(module, now_target):
            next_module = getattr(module, now_target)
            return self.search_target(next_module, target_names)
        else:
            CACodeLog.err(ImportError,
                          e_fields.CACode_Factory_Error(
                              f"""The package name does not exist in the search tree: {now_target}, please check whether the package name is filled in correctly"""))
