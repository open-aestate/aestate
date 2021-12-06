# -*- utf-8 -*-
import math
import os
import threading
import time
from collections import OrderedDict
from enum import Enum
from typing import List

import psutil

from aestate.exception import LogStatus
from aestate.util import others
from aestate.util.others import write
from aestate.work.Modes import Singleton

"""
全世界无产者,联合起来!!!
我们要强烈抵制资本主义的剥削!!!
"""


class CacheStatus(Enum):
    """
    缓存的状态
    """
    CLOSE = 0
    OPEN = 1


class SqlCacheItem(object):
    """缓存对象"""

    def __init__(self, key, value, instance):
        # 执行的sql
        self.sql = key
        # 数据
        self.data = value
        self.instance = instance
        # 使用次数
        self.using_count = 0
        # 写入的时间
        self.create_time = time.time()
        self.last_using_time = time.time()
        super(SqlCacheItem, self).__init__()

    def __setattr__(self, key, value):
        if key == 'using_count':
            self.last_using_time = time.time()
        super(SqlCacheItem, self).__setattr__(key, value)

    def set_using_count(self):
        self.using_count += 1

    def get_sql(self):
        return self.sql

    def get_value(self):
        return self.data


class DataContainer(List[SqlCacheItem]):
    def __init__(self):
        list.__init__([])
        self.data_dict = {}

    def __sizeof__(self):
        return sum(i.__sizeof__() for i in self)

    def delete(self, tb_name):
        temp_array = []
        for i, item in enumerate(self):
            if hasattr(item, 'instance') and item.instance.get_tb_name() == tb_name:
                temp_array.append(i)
            elif item.instance.get_tb_name() == tb_name:
                temp_array.append(i)
        temp_array = list(reversed(temp_array))
        while len(temp_array):
            del self[temp_array[0]]
            del temp_array[0]


class SqlCacheManage(object):
    """
    缓存管理

    1.当内存满足系统运行内存的1/10时,满足最大限度数据内容,保证数据完整性的同时保留数据

    2.当单次查询数据大于阈值时,保留数据并不在扩大缓存空间,数据完整保留,但不再清理,直到处于第二缓存空间更多查询数据量再次大于阈值时清理

    3.当通过aestate改变数据时记录数据变更信息,并重新将数据写入缓存,移除旧缓存数据,这将意味着非通过aestate修改的数据不可被检测到

    4.扩容策略:当前内存>=当前容量1/2时,重新计算查询数据量

    5.流量计算方式:当前缓存大小 + (当前缓存大小 / 上次扩容时间至当前时间段内插入的新内容数量) ** 2

    6.移除方案:时间段内缓存查询次数最少内存最大优先,当 (A次数-B次数) * 10 <= (A占用内存-B占用内存),优先删除B
    """
    # 初始内存大小为1024Byte
    __capacity_max__ = 1024
    # 系统运行时计算得到的内存阈值
    __max__ = psutil.virtual_memory().free / 10
    _instance_lock = threading.RLock()
    # 容器
    __data_container__ = DataContainer()
    # 缓存的状态
    status = CacheStatus.OPEN

    def __contains__(self, o: str) -> bool:
        """判断缓存中是否存在这个sql的查询记录"""
        data = self.get_container()
        if len(data) == 0:
            return False
        for item in data:
            if item.sql == o:
                return True
        return False

    def get_size(self):
        """获取当前缓存的大小"""
        return self.get_container_size()

    def get_max(self):
        return self.__max__

    def need_calculate(self):
        """是否需要清理缓存"""
        return self.get_capacity_max() / 2 <= self.get_size()

    def calculate_ram(self) -> bool:
        """扩容"""
        self.reset_max_ram()
        if self.need_calculate():
            target_ram = int(self.get_capacity_max() * 2 + self.get_size())
            if target_ram < self.get_max():
                self.__capacity_max__ = target_ram
                return True
            else:
                # 直接等于最大内存,然后清理一下
                self.__capacity_max__ = self.get_max()
                # 当前允许的最大内存的20%(缓存的平均值),直到缓存满足
                size = math.ceil((self.get_capacity_max() * 0.2) / (self.get_size() / len(self.get_container())))
                if size != 0:
                    while size:
                        del self.__data_container__[0]
                        size -= 1
                return True
        else:
            return False

    def get(self, sql) -> SqlCacheItem:
        """获取一条sql"""
        index = self.index(sql)
        ci = self.get_container()[index]
        ci.set_using_count()
        self.sort_data()
        return ci

    def remove(self, sql):
        """移除某个sql的缓存"""
        index = self.index(sql)
        if index != -1:
            del self.__data_container__[index]

    def remove_by_instance(self, tb_name):
        """根据instance的表来删除缓存"""
        self.get_container().delete(tb_name)

    def clean_up(self):
        """清理缓存,不是清除缓存,清理是清理使用次数不多的缓存"""
        if self.need_calculate():
            # 先试图扩容
            self.calculate_ram()

    def reset_max_ram(self):
        """重新计算当前可用的最大缓存"""
        free_ram = psutil.virtual_memory().free
        self.__max__ = int(free_ram / 10)

    def sort_data(self):
        # 重新排序
        self.__data_container__.sort(key=lambda x: x.using_count)

    def set(self, sql, value, instance):
        self.__data_container__.append(SqlCacheItem(key=sql, value=value, instance=instance))
        # 判断缓存是否已经满了
        self.clean_up()
        self.sort_data()

    def get_container(self) -> DataContainer:
        return self.__data_container__

    def get_container_size(self):
        return self.__data_container__.__sizeof__()

    def get_capacity_max(self):
        """获取当前内存允许的最大限制"""
        return self.__capacity_max__

    def clear(self):
        """清空缓存,谨慎操作
        如果仅仅是需要清理缓存空间,请使用clean_up()函数
        """
        self.__data_container__.clear()

    def index(self, sql):
        """验证sql是否存在缓存"""
        for index, item in enumerate(self.get_container()):
            if item.sql == sql:
                return index
        return -1

    def __new__(cls, *args, **kwargs):
        """
        单例管理缓存内容
        """
        instance = Singleton.createObject(cls)
        return instance


class PojoContainer:
    """对象管理器"""

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
    """单个对象的容器"""

    def __init__(self, _type, _object):
        super(PojoItemCache).__init__()
        self._type = _type
        self._object = _object


class PojoManage:
    """管理pojo的缓存"""
    _instance_lock = threading.RLock()
    pojo_list = PojoContainer()

    def append(self, _cls_name: type, _object):
        self.pojo_list + PojoItemCache(_type=_cls_name, _object=_object)

    @staticmethod
    def get(_cls, *args, **kwargs):
        if 'new' in kwargs.keys():
            return object.__new__(_cls)
        this = PojoManage()
        _class_object_ = object.__new__(_cls)
        cls_name = others.fullname(_class_object_)
        _obj = this.pojo_list.get(cls_name)
        if _obj is None:
            this.append(cls_name, _class_object_)
            _obj = this.pojo_list.get(cls_name)
        [setattr(_obj, k, v) for k, v in kwargs.items()]
        return _obj

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance


class LogCache:
    _instance_lock = threading.RLock()
    # 是否已经显示logo了
    info_logo_show = False
    warn_logo_show = False
    error_logo_show = False
    # 文件名,当满足最大时将会使用一个新的文件作为储存日志
    info_file_name = []
    warn_file_name = []
    error_file_name = []

    def get_filename(self, path, max_clear, status):

        if status == LogStatus.Info:
            center_name = 'info'
            oa = self.info_file_name
            logo_show = 'info_logo_show'
        elif status == LogStatus.Error:
            center_name = 'error'
            oa = self.warn_file_name
            logo_show = 'error_logo_show'
        elif status == LogStatus.Warn:
            center_name = 'warn'
            oa = self.error_file_name
            logo_show = 'warn_logo_show'
        else:
            center_name = 'info'
            oa = self.info_file_name
            logo_show = 'info_logo_show'

        _path = os.path.join(path, center_name)
        if len(oa) == 0:
            oa.append(others.date_format(fmt='%Y.%m.%d.%H.%M.%S') + '.log')
            setattr(self, logo_show, False)
        else:
            if not os.path.exists(os.path.join(_path, oa[len(oa) - 1])):
                write(os.path.join(_path, '.temp'), '')
                setattr(self, logo_show, False)
            if os.path.getsize(os.path.join(_path, oa[len(oa) - 1])) >= max_clear:
                oa.append(others.date_format(fmt='%Y.%m.%d.%H.%M.%S') + '.log')
                setattr(self, logo_show, False)

        return os.path.join(center_name, oa[len(oa) - 1])

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance
