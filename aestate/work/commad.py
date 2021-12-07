# -*- utf-8 -*-
# encoding:utf-8
# @Time: 2021/6/27 20:47
# @Author: CACode
# 版本有三种状态 正式版从1.0.0往后逐个加 1,对应版本的补丁为'a+补丁次数'
__version__ = '1.0.5a2'
__description__ = "Aestate framework for Python,You can see:https://gitee.com/aecode/aestate"
__author__ = "CACode"
__author_email__ = "cacode@163.com"
__url__ = "https://gitee.com/aecode/aestate"
__issues__ = 'https://gitee.com/aecode/aestate/issues'
__license__ = 'Apache License 2.0'
__project_name__ = 'Aestate'
__logo__ = """
         :: Aestate Framework ::      (version:%s)
    +    __                    _        _        __    +
    +   / /     /\            | |      | |       \ \   +
    +  / /     /  \   ___  ___| |_ __ _| |_ ___   \ \  +
    + | |     / /\ \ / _ \/ __| __/ _` | __/ _ \   | | +
    +  \ \   / ____ \  __/\__ \ || (_| | ||  __/  / /  +
========\_\=/_/====\_\___||___/\__\__,_|\__\___|=/_/========
""" % __version__

__log_logo__ = """
         :: Aestate Framework ::      (version:%s)
       __      ____    ___    ____      __      ____    ____ 
      /__\    ( ___)  / __)  (_  _)    /__\    (_  _)  ( ___)
     /(__)\    )__)   \__ \    )(     /(__)\     )(     )__) 
    (__)(__)  (____)  (___/   (__)   (__)(__)   (__)   (____)
""" % __version__

import importlib

try:
    from prettytable import PrettyTable
except ModuleNotFoundError as e:
    print("请先安装 [prettytable] 再执行 [-h] 命令,使用 [pip install prettytable]")


class Commands:
    def __init__(self, *args):
        """
        下面的@staticmethod主要是为了不想看见黄线警告，并没有其他意思
        """
        self.args = args
        self.c = {
            "": (
                self.start,
                '显示aestate的logo和版本号，用于检查aestate是否安装成功',
                "aestate"
            ),
            "-v": (
                self.version,
                "显示aestate的版本号",
                "aestate -v"
            ),
            "-create": (
                self.create,
                "将文件内存在pojo对象的类生成到数据库中称为数据库的表"
                "数据库格式化类型参考默认的 [mysql] 格式",
                'aestate -create [文件名] [数据库类型 (可选)]'
            ),
            "-m": (
                self.make,
                "将数据库中的表同步生成到当前目录下的 [model.py]，并默认命名为 [数据库命_表名]",
                'aestate -m [--n [生成的文件名 (可选) ]] [--nn [生成的类名 (可选)]]'
            ),
            "-enc": (
                self.enc,
                "加密模型",
                'aestate -enc [密码]'
            ),
            "-dec": (
                self.dec,
                "解密模型",
                'aestate -dec [被加密后的文件] [密码]'
            ),
            "-check": (
                self.check,
                "检查模型与数据库中的表结构是否一直",
                'aestate -check [文件名] [数据库名]'
            ),
            "-h": (
                self.help,
                "帮助文档",
                'aestate -h'
            ),
            "-startproject": (
                self.startproject,
                "创建一个web项目",
                'aestate -startproject 项目名'
            )
        }

    def startproject(self):
        pass

    def start(self):
        print(__logo__)

    def create(self):
        print(__logo__)
        try:
            file = self.args[2]
            db_name = self.args[3]
        except IndexError:
            raise IndexError("为了保证数据库的sql执行顺利，请填写pojo存在的文件名和数据库名称")
        import inspect
        temp_module = importlib.import_module(file)

        temp_classes = inspect.getmembers(temp_module, inspect.isclass)
        for name, class_ in temp_classes:
            c = class_()
            c.orm.create()

    def enc(self):
        pass

    def dec(self):
        pass

    def version(self):
        print(__version__)

    def make(self):
        pass

    def check(self):
        print(__logo__)
        try:
            file = self.args[2]
            db_name = self.args[3]
        except IndexError:
            raise IndexError("为了保证数据库的sql执行顺利，请填写pojo存在的文件名和数据库名称")
        import inspect
        temp_module = importlib.import_module(file)

        temp_classes = inspect.getmembers(temp_module, inspect.isclass)
        for name, class_ in temp_classes:
            c = class_()
            c.orm.check()

    def help(self):
        table = PrettyTable(["命令", "使用方法", "描述"])
        table.border = True
        table.junction_char = '-'
        [table.add_row([k, v[2], v[1]]) for k, v in self.c.items()]
        print(table)
