import threading

from CACodeFramework.cacode import Modes
from CACodeFramework.exception import e_fields
from CACodeFramework.opera.CompulsoryRun import Compulsory
from CACodeFramework.util.Log import CACodeLog
import importlib


class Factory(object):
    _instance_lock = threading.Lock()

    def __init__(self, modules):
        try:
            self.modules = modules
        except AttributeError:
            CACodeLog.err(SyntaxError, e_fields.CACode_Factory_Error(
                'Please import the Pojo module first,请先设置导入modules模块'))

        self.module_names = {}
        self.__base_init__()

    def __base_init__(self):
        for package_name in self.modules:
            base_module = str(package_name).split('.')
            last_name = base_module[
                (len(base_module) - 1) if
                len(base_module) > 0 else
                CACodeLog.err(TypeError,
                              e_fields.CACode_Factory_Error(
                                  'The module cannot be found, perhaps the `instances` are not set,'
                                  '找不到模块，也许是未设置`instances`')
                              )
            ]
            # 将包导入
            self.module_names[last_name] = package_name

    @classmethod
    def createInstance(cls, name: str, *args, **kwargs):
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
            ins = MyFactory.createInstance("Demo.DemoTable",kwargs={})
            print(ins)




        :param name:类的名称,从配置的instances开始获得
        :param args:类的附属参数
        :param kwargs:类的附属参数
        """

        # 使用单例模式初始化仓库
        this = Modes.Singleton.createFactory(cls)

        module_names = str(name).split('.')
        first_module = module_names[0]
        del module_names[0]

        assert len(module_names) > 0

        import_module = importlib.import_module(this.module_names[first_module])

        result = this.search_target(import_module, module_names)

        end_obj = Compulsory.run_function(func=result, args=args, kwargs=kwargs)

        return end_obj

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
                              f'The package name does not exist in the search tree: {now_target}, please check '
                              'whether the package name is filled in correctly'))
