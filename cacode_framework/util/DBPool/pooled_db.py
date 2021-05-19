from threading import Condition

from . import __version__
from .steady_db import connect


class PooledDBError(Exception):
    """General PooledDB error."""


class InvalidConnection(PooledDBError):
    """Database connection is invalid."""


class NotSupportedError(PooledDBError):
    """DB-API module not supported by PooledDB."""


class TooManyConnections(PooledDBError):
    """Too many database connections were opened."""


class PooledDB:
    """Pool for DB-API 2 connections.

    After you have created the connection pool, you can use
    connection() to get pooled, steady DB-API 2 connections.
    """

    version = __version__

    def __init__(
            self, creator, mincached=0, maxcached=0,
            maxshared=0, maxconnections=0, blocking=False,
            maxusage=None, setsession=None, reset=True,
            failures=None, ping=1,
            *args, **kwargs):
        """

        设置DB-API 2连接池。

        creator：返回新的DB-API 2的任意函数
            连接对象或符合DB-API 2的数据库模块
        mincached：池中空闲连接的初始数量
            （0表示启动时未建立连接）
        maxcached：池中最大空闲连接数
            （0或无表示池大小不受限制）
        maxshared：共享连接的最大数量
            （0或无表示所有连接都是专用的）
            当达到此最大数量时，连接为
            如果被要求共享，则将它们共享。
        maxconnections：通常允许的最大连接数
            （0或无表示任意数量的连接）
        blocking：确定超出最大值时的行为
            （如果将其设置为true，请阻止并等待，直到
            连接减少，否则将报告错误）
        maxusage：单个连接的最大重用次数
            （0或无表示无限重用）
            当达到连接的最大使用次数时，
            连接将自动重置（关闭并重新打开）。
        setsession：可用于准备的SQL命令的可选列表
            会话，例如[“将日期样式设置为...”，“将时区设置为...”]
        reset：返回到池后应如何重置连接
            （对于以begin（）开始的回滚事务，为False或None，
            出于安全考虑，总是发出回滚是正确的）
        failures：可选的异常类或异常类的元组
            为此，应应用连接故障转移机制，
            如果默认值（OperationalError，InternalError）不足够
        ping：确定何时应使用ping（）检查连接
            （0 =无=永不，1 =默认=每当从池中获取时，
            2 =创建游标时，4 =执行查询时，
            7 =始终，以及这些值的所有其他位组合）
        args，kwargs：应传递给创建者的参数
            函数或DB-API 2模块的连接构造函数


        初始化配置
        以下参数与PooledDB一致
        :param creator:默认即可
        :param maxconnections:默认即可
        :param mincached:默认即可
        :param maxcached:默认即可
        :param maxshared:默认即可
        :param blocking:默认即可
        :param setsession:默认即可
        :param ping:默认即可
        :param host:数据库IP地址
        :param port:端口
        :param user:用户名,如root
        :param password:密码
        :param database:数据库名
        :param charset:编码格式
        :param POOL:使用自定义的PooledDB,不建议
        """
        try:
            threadsafety = creator.threadsafety
        except AttributeError:
            try:
                if not callable(creator.connect):
                    raise AttributeError
            except AttributeError:
                threadsafety = 2
            else:
                threadsafety = 0
        if not threadsafety:
            raise NotSupportedError("数据库模块未分配线程安全")
        self._creator = creator
        self._args, self._kwargs = args, kwargs
        self._blocking = blocking
        self._maxusage = maxusage
        self._setsession = setsession
        self._reset = reset
        self._failures = failures
        self._ping = ping
        if mincached is None:
            mincached = 0
        if maxcached is None:
            maxcached = 0
        if maxconnections is None:
            maxconnections = 0
        if maxcached:
            if maxcached < mincached:
                maxcached = mincached
            self._maxcached = maxcached
        else:
            self._maxcached = 0
        if threadsafety > 1 and maxshared:
            self._maxshared = maxshared
            self._shared_cache = []  # 共享连接的缓存
        else:
            self._maxshared = 0
        if maxconnections:
            if maxconnections < maxcached:
                maxconnections = maxcached
            if maxconnections < maxshared:
                maxconnections = maxshared
            self._maxconnections = maxconnections
        else:
            self._maxconnections = 0
        self._idle_cache = []  # 空闲连接池
        self._lock = Condition()
        self._connections = 0
        # Establish an initial number of idle database connections:
        idle = [self.dedicated_connection() for i in range(mincached)]
        while idle:
            idle.pop().close()

    def steady_connection(self):
        """获得稳定的，未池化的DB-API 2连接."""
        return connect(
            self._creator, self._maxusage, self._setsession,
            self._failures, self._ping, True, *self._args, **self._kwargs)

    def connection(self, shareable=True):
        """从连接池中获得稳定的缓存的DB-API 2连接。

         :param shareable:允许共享连接
        """
        if shareable and self._maxshared:
            self._lock.acquire()
            try:
                while (not self._shared_cache and self._maxconnections
                       and self._connections >= self._maxconnections):
                    self._wait_lock()
                if len(self._shared_cache) < self._maxshared:
                    # shared cache is not full, get a dedicated connection
                    try:  # first try to get it from the idle cache
                        con = self._idle_cache.pop(0)
                    except IndexError:  # else get a fresh connection
                        con = self.steady_connection()
                    else:
                        con._ping_check()  # check this connection
                    con = SharedDBConnection(con)
                    self._connections += 1
                else:  # shared cache full or no more connections allowed
                    self._shared_cache.sort()  # least shared connection first
                    con = self._shared_cache.pop(0)  # get it
                    while con.con._transaction:
                        # do not share connections which are in a transaction
                        self._shared_cache.insert(0, con)
                        self._wait_lock()
                        self._shared_cache.sort()
                        con = self._shared_cache.pop(0)
                    con.con._ping_check()  # check the underlying connection
                    con.share()  # increase share of this connection
                # put the connection (back) into the shared cache
                self._shared_cache.append(con)
                self._lock.notify()
            finally:
                self._lock.release()
            con = PooledSharedDBConnection(self, con)
        else:  # try to get a dedicated connection
            self._lock.acquire()
            try:
                while (self._maxconnections
                       and self._connections >= self._maxconnections):
                    self._wait_lock()
                # connection limit not reached, get a dedicated connection
                try:  # first try to get it from the idle cache
                    con = self._idle_cache.pop(0)
                except IndexError:  # else get a fresh connection
                    con = self.steady_connection()
                else:
                    con._ping_check()  # check connection
                con = PooledDedicatedDBConnection(self, con)
                self._connections += 1
            finally:
                self._lock.release()
        return con

    def dedicated_connection(self):
        """Alias for connection(shareable=False)."""
        return self.connection(False)

    def unshare(self, con):
        """Decrease the share of a connection in the shared cache."""
        self._lock.acquire()
        try:
            con.unshare()
            shared = con.shared
            if not shared:  # connection is idle,
                try:  # so try to remove it
                    self._shared_cache.remove(con)  # from shared cache
                except ValueError:
                    pass  # pool has already been closed
        finally:
            self._lock.release()
        if not shared:  # connection has become idle,
            self.cache(con.con)  # so add it to the idle cache

    def cache(self, con):
        """Put a dedicated connection back into the idle cache."""
        self._lock.acquire()
        try:
            if not self._maxcached or len(self._idle_cache) < self._maxcached:
                con._reset(force=self._reset)  # rollback possible transaction
                # the idle cache is not full, so put it there
                self._idle_cache.append(con)  # append it to the idle cache
            else:  # if the idle cache is already full,
                con.close()  # then close the connection
            self._connections -= 1
            self._lock.notify()
        finally:
            self._lock.release()

    def close(self):
        """Close all connections in the pool."""
        self._lock.acquire()
        try:
            while self._idle_cache:  # close all idle connections
                con = self._idle_cache.pop(0)
                try:
                    con.close()
                except Exception:
                    pass
            if self._maxshared:  # close all shared connections
                while self._shared_cache:
                    con = self._shared_cache.pop(0).con
                    try:
                        con.close()
                    except Exception:
                        pass
                    self._connections -= 1
            self._lock.notifyAll()
        finally:
            self._lock.release()

    def __del__(self):
        """Delete the pool."""
        try:
            self.close()
        except:  # builtin Exceptions might not exist any more
            pass

    def _wait_lock(self):
        """Wait until notified or report an error."""
        if not self._blocking:
            raise TooManyConnections
        self._lock.wait()


# Auxiliary classes for pooled connections

class PooledDedicatedDBConnection:
    """Auxiliary proxy class for pooled dedicated connections."""

    def __init__(self, pool, con):
        """Create a pooled dedicated connection.

        pool: the corresponding PooledDB instance
        con: the underlying SteadyDB connection
        """
        # basic initialization to make finalizer work
        self._con = None
        # proper initialization of the connection
        if not con.threadsafety():
            raise NotSupportedError("数据库模块未分配线程安全")
        self._pool = pool
        self._con = con

    def close(self):
        """Close the pooled dedicated connection."""
        # Instead of actually closing the connection,
        # return it to the pool for future reuse.
        if self._con:
            self._pool.cache(self._con)
            self._con = None

    def __getattr__(self, name):
        """Proxy all members of the class."""
        if self._con:
            return getattr(self._con, name)
        else:
            raise InvalidConnection

    def __del__(self):
        """Delete the pooled connection."""
        try:
            self.close()
        except:  # builtin Exceptions might not exist any more
            pass


class SharedDBConnection:
    """Auxiliary class for shared connections."""

    def __init__(self, con):
        """Create a shared connection.

        con: the underlying SteadyDB connection
        """
        self.con = con
        self.shared = 1

    def __lt__(self, other):
        if self.con._transaction == other.con._transaction:
            return self.shared < other.shared
        else:
            return not self.con._transaction

    def __le__(self, other):
        if self.con._transaction == other.con._transaction:
            return self.shared <= other.shared
        else:
            return not self.con._transaction

    def __eq__(self, other):
        return (self.con._transaction == other.con._transaction
                and self.shared == other.shared)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return other.__lt__(self)

    def __ge__(self, other):
        return other.__le__(self)

    def share(self):
        """Increase the share of this connection."""
        self.shared += 1

    def unshare(self):
        """Decrease the share of this connection."""
        self.shared -= 1


class PooledSharedDBConnection:
    """Auxiliary proxy class for pooled shared connections."""

    def __init__(self, pool, shared_con):
        """Create a pooled shared connection.

        pool: the corresponding PooledDB instance
        con: the underlying SharedDBConnection
        """
        # basic initialization to make finalizer work
        self._con = None
        # proper initialization of the connection
        con = shared_con.con
        if not con.threadsafety() > 1:
            raise NotSupportedError("数据库模块未分配线程安全")
        self._pool = pool
        self._shared_con = shared_con
        self._con = con

    def close(self):
        """Close the pooled shared connection."""
        # Instead of actually closing the connection,
        # unshare it and/or return it to the pool.
        if self._con:
            self._pool.unshare(self._shared_con)
            self._shared_con = self._con = None

    def __getattr__(self, name):
        """Proxy all members of the class."""
        if self._con:
            return getattr(self._con, name)
        else:
            raise InvalidConnection

    def __del__(self):
        """Delete the pooled connection."""
        try:
            self.close()
        except:  # builtin Exceptions might not exist any more
            pass
