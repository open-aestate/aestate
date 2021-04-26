# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        Modes
# Author:           CACode
# Version:          1.2
# Created:          2021/4/27
# Description:      Main Function:    所有用到的设计模式
#                   此文件内保存可外置的设计模式,用于让那些脑瘫知道我写的框架用了什么设计模式而不是
#                   一遍一遍问我这框架都用了什么设计模式、体现在哪里,我叼你妈
# Class List:    Singleton -- 单例模式
# History:
#       <author>        <version>       <time>      <desc>
#       CACode         1.2          2021/4/27  00:43    将设计模式迁移到此文件内
# ------------------------------------------------------------------

class Singleton:
    """
    使用工厂模式
    """

    @staticmethod
    def create(cls):
        with cls._instance_lock:
            if not hasattr(cls, "__instance__"):
                cls.__instance__ = cls(cls.modules)
        return cls.__instance__
