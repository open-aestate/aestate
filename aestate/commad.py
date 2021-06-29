# -*- utf-8 -*-
# encoding:utf-8
# @Time: 2021/6/27 20:47
# @Author: CACode

__version__ = '1.0.1b3'
__description__ = "Aestate framework for Python,You can see:https://gitee.com/cacode_cctvadmin/aestate"
__author__ = "CACode"
__author_email__ = "cacode@163.com"
__url__ = "https://gitee.com/cacode_cctvadmin/aestate"
__aestate__ = __version__, {'aestate-json': '1.0.0'}
__license__ = 'Apache License 2.0'
__name__ = 'aestate'
__logo__ = """
        __                    _        _        __   
       / /     /\            | |      | |       \ \  
      / /     /  \   ___  ___| |_ __ _| |_ ___   \ \ 
     < <     / /\ \ / _ \/ __| __/ _` | __/ _ \   > >
      \ \   / ____ \  __/\__ \ || (_| | ||  __/  / / 
       \_\ /_/    \_\___||___/\__\__,_|\__\___| /_/  

       :: Aestate Framework ::      (version:%s)

    """ % __version__
try:
    from prettytable import PrettyTable
except:
    print("请先安装 [prettytable] 再执行 [-h] 命令,使用 [pip install prettytable]")
    exit(1)


class Commands:
    def __init__(self):
        self.c = {
            "": (
                self.__start,
                '显示aestate的logo和版本号，用于检查aestate是否安装成功',
                "aestate"
            ),
            "-v": (
                self.__version,
                "显示aestate的版本号",
                "aestate -v"
            ),
            "-c": (
                self.__make,
                "将文件内存在pojo对象的类生成到数据库中成为数据库的表",
                'aestate -c [文件名] [数据库类型 (可选)]'
            ),
            "-m": (
                self.__help,
                "将数据库中的表同步生成到当前目录下的 [model.py]，并默认命名为 [数据库命_表名]",
                'aestate -m [--n [生成的文件名 (可选) ]] [--nn [生成的类名 (可选)]]'
            ),
            "-enc": (
                self.__help,
                "加密模型",
                'aestate -enc [密码]'
            ),
            "-dec": (
                self.__help,
                "帮助文档",
                'aestate -dec [被加密后的文件] [密码]'
            ),
            "-h": (
                self.__help,
                "帮助文档",
                'aestate -h'
            ),
        }

    def __start(self):
        print(__logo__)

    @staticmethod
    def __version():
        print(__aestate__)

    def __make(self):
        pass

    def __help(self):
        table = PrettyTable(["命令", "使用方法", "描述"])
        table.border = True
        table.junction_char = '-'
        [table.add_row([k, v[2], v[1]]) for k, v in self.c.items()]
        print(table)


class Start:
    def __init__(self, **kwargs):
        """
        所有操作的父类
        """
        for k, v in kwargs.items():
            setattr(self, k, v)

    def create(self, filename, db_type):
        pass
