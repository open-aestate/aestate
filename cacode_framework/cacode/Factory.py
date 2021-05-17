import threading

from CACodeFramework.cacode import Modes
from CACodeFramework.exception import e_fields
from CACodeFramework.exception.e_fields import ModuleCreateError
from CACodeFramework.opera.CompulsoryRun import Compulsory
from CACodeFramework.util.Log import CACodeLog
import importlib


class Factory(object):
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
    """
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

        创建一个实例对象,并提供ORM操作

        name使用包名最后一位置作为起始值,如:

                Test.models.Demo

        那么,当你调用Demo下的model时,你必须使用`Demo.DemoTable`这种

        格式,因为包的引导使用的键是`.`(点)最后一位参数作为键



        :param name:类的名称,从配置的instances开始获得
        :param args:类的附属参数
        :param kwargs:类的附属参数
        """

        # 使用单例模式初始化仓库
        this = Modes.Singleton.createFactory(cls)

        module_names = str(name).split('.')

        # 断言这个module name不为空
        if len(module_names) < 0:
            CACodeLog.log_error(msg='The name`s address of the module should be greater than or equal to 2',
                                obj=ModuleCreateError,
                                raise_exception=True)

        first_module = module_names[0]

        del module_names[0]

        import_module = importlib.import_module(this.module_names[first_module])

        result = Compulsory.search_target(import_module, module_names)

        end_obj = Compulsory.run_function(func=result, args=args, kwargs=kwargs)

        return end_obj
