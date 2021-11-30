# -*- utf-8 -*-
import os
import threading
from collections import OrderedDict
from enum import Enum
from typing import List

from aestate.exception import LogStatus
from aestate.util import others
from aestate.util.others import write
from aestate.work.Modes import Singleton


class CacheStatus(Enum):
    CLOSE = 0
    OPEN = 1


class SqlCacheItem(object):
    """缓存对象"""

    def __init__(self, key, value):
        self.sql = key
        self.data = value
        self.__using_count__ = 0
        super(SqlCacheItem, self).__init__()

    def get_sql(self):
        return self.sql

    def get_value(self):
        return self.data


class SqlCacheManage(object):
    """
    缓存管理

    1.当内存满足系统运行内存的1/10时,满足最大限度数据内容,保证数据完整性的同时保留数据

    2.当单次查询数据大于阈值时,保留数据并不在扩大缓存空间,数据完整保留,但不再清理,直到处于第二缓存空间更多查询数据量再次大于阈值时清理

    3.当通过aestate改变数据时记录数据变更信息,并重新将数据写入缓存,移除旧缓存数据,这将意味着非通过aestate修改的数据不可被检测到

    4.扩容策略:当前内存>=当前容量1/2时,重新计算查询数据量

    5.流量计算方式:当前缓存大小 + (当前缓存大小 / 上次扩容时间至当前时间段内插入的新内容数量) * 2 * 当前缓存大小

    6.移除方案:时间段内缓存查询次数最少内存最大优先,当 (A次数-B次数) * 10 <= (A占用内存-B占用内存),优先删除B
    """
    # 初始内存大小为1024Byte
    __capacity_max__ = 1024
    # 系统运行时计算得到的内存阈值
    __max__ = 0
    _instance_lock = threading.RLock()
    # 容器
    __data_container__ = []
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

    def get(self, key) -> SqlCacheItem:
        for item in self.get_container():
            if item.sql == key:
                item.__using_count__ += 1
                return item

    def set(self, sql, value):
        self.__data_container__.append(SqlCacheItem(key=sql, value=value))

    def get_container(self) -> List[SqlCacheItem]:
        return self.__data_container__

    def get_capacity_max(self):
        """获取当前内存允许的最大限制"""
        return self.__capacity_max__

    def clear(self):
        """清空缓存,谨慎操作"""
        self.__data_container__.clear()

    def verify(self, sql):
        """验证sql是否存在缓存"""
        pass

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
