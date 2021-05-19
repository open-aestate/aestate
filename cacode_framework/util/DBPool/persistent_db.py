from . import __version__
from .steady_db import connect

try:
    # 纯python实现的thread lock
    from _threading_local import local
except ImportError:
    # 默认版本的thread locak
    from threading import local


class PersistentDBError(Exception):
    """General PersistentDB error."""


class NotSupportedError(PersistentDBError):
    """DB-API module not supported by PersistentDB."""


class PersistentDB:
    """生成基于db-api2的数据库连接池对象
    """

    version = __version__

    def __init__(
            self, creator,
            maxusage=None, setsession=None, failures=None, ping=1,
            closeable=False, threadlocal=None, *args, **kwargs):
        """
        设置持久性DB-API 2连接生成器。

        创建者：返回新的DB-API 2的任意函数
            连接对象或符合DB-API 2的数据库模块
        maxusage：连接池最大数量，0表示无限
        setsession：可用于准备的SQL命令的可选列表
            会话，例如[“将日期样式设置为...”，“将时区设置为...”]
        失败：可选的异常类或异常类的元组
            为此，应应用连接故障转移机制，
            如果默认值（OperationalError，InternalError）不足够
        ping：确定何时应使用ping（）检查连接
            （0 =无=永不，1 =默认=每当被请求时，
            2 =创建游标时，4 =执行查询时，
            7 =始终，以及这些值的所有其他位组合）
        closeable：设置为True将允许被关闭
        threadlocal：线程独立
        """
        try:
            threadsafety = creator.threadsafety
        except AttributeError:
            try:
                if not callable(creator.connect):
                    raise AttributeError
            except AttributeError:
                threadsafety = 1
            else:
                threadsafety = 0
        if not threadsafety:
            raise NotSupportedError("数据库模块未分配线程安全")
        self._creator = creator
        self._maxusage = maxusage
        self._setsession = setsession
        self._failures = failures
        self._ping = ping
        self._closeable = closeable
        self._args, self._kwargs = args, kwargs
        self.thread = (threadlocal or local)()

    def steady_connection(self):
        """Get a steady, non-persistent DB-API 2 connection."""
        return connect(
            self._creator, self._maxusage, self._setsession,
            self._failures, self._ping, self._closeable,
            *self._args, **self._kwargs)

    def connection(self, shareable=False):
        """共享连接
        长时间未关闭则不会被共享
        """
        try:
            con = self.thread.connection
        except AttributeError:
            con = self.steady_connection()
            if not con.threadsafety():
                raise NotSupportedError("数据库模块未分配线程安全")
            self.thread.connection = con
        con._ping_check()
        return con

    def dedicated_connection(self):
        """Alias for connection(shareable=False)."""
        return self.connection()
