# -*- utf-8 -*-
import threading
from collections import OrderedDict
from typing import List

from aestate.util import others
from aestate.work.Modes import Singleton


class CacheItem(OrderedDict):
    """缓存对象"""

    def __init__(self, key, value):
        super(CacheItem, self).__init__()


class CacheManage(List):
    """
    缓存管理

    1.当内存满足系统运行内存的1/10时,满足最大限度数据内容,保证数据完整性的同时保留数据

    2.当单次查询数据大于阈值时,保留数据并不在扩大缓存空间,数据完整保留,但不再清理,直到处于第二缓存空间更多查询数据量再次大于阈值时清理

    3.当通过aestate改变数据时记录数据变更信息,并重新将数据写入缓存,移除旧缓存数据,这将意味着非通过aestate修改的数据不可被检测到

    4.扩容策略:当前内存>=当前容量1/2时,重新计算查询数据量

    5.流量计算方式:当前缓存大小 + (当前缓存大小 / 上次扩容时间至当前时间段内插入的新内容数量) * 2 * 当前缓存大小

    6.移除方案:时间段内缓存查询次数最少内存最大优先,当 (A次数-B次数) * 10 <= (A占用内存-B占用内存),优先删除B
    """

    def __init__(self):
        # 初始内存大小为256byte
        super(CacheManage).__init__([])
        self.capacity = 256

    def __new__(cls, *args, **kwargs):
        """
        单例管理缓存内容
        """
        instance = Singleton.createDbOpera(cls)
        return instance

    def clean(self):
        pass


class PojoContainer:
    def __init__(self):
        self.solvent = []

    def __add__(self, __object):
        self.solvent.append(__object)

    @property
    def size(self) -> int:
        return len(self.solvent)

    def get(self, name):
        for item in self.solvent:
            if item._type == name:
                return item._object
        return None


class PojoItemCache(OrderedDict):
    def __init__(self, _type, _object):
        super(PojoItemCache).__init__()
        self._type = _type
        self._object = _object


class PojoManage:
    """管理pojo的缓存"""
    _instance_lock = threading.RLock()

    def __init__(self):
        self.pojo_list = PojoContainer()

    def append(self, _object: type):
        _obj = object.__new__(_object)
        cls_name = others.fullname(_obj)
        self.pojo_list + PojoItemCache(_type=cls_name, _object=_obj)

    @staticmethod
    def get(_cls, *args, **kwargs):
        this = PojoManage()
        cls_name = others.fullname(_cls)
        o = this.pojo_list.get(cls_name)
        if o is None:
            this.append(_cls)
        return this.pojo_list.get(cls_name).copy(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createDbOpera(cls)
        return instance
