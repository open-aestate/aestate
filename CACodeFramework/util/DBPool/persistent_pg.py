from . import __version__
from .steady_pg import SteadyPgConnection

try:
    from _threading_local import local
except ImportError:
    from threading import local


class PersistentPg:
    """Generator for persistent classic PyGreSQL connections.

    After you have created the connection pool, you can use
    connection() to get thread-affine, steady PostgreSQL connections.
    """

    version = __version__

    def __init__(
            self, maxusage=None, setsession=None,
            closeable=False, threadlocal=None, *args, **kwargs):
        """Set up the persistent PostgreSQL connection generator.

        maxusage: maximum number of reuses of a single connection
            (0 or None means unlimited reuse)
            When this maximum usage number of the connection is reached,
            the connection is automatically reset (closed and reopened).
        setsession: optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        closeable: if this is set to true, then closing connections will
            be allowed, but by default this will be silently ignored
        threadlocal: an optional class for representing thread-local data
            that will be used instead of our Python implementation
            (threading.local is faster, but cannot be used in all cases)
        args, kwargs: the parameters that shall be used to establish
            the PostgreSQL connections using class PyGreSQL pg.DB()
        """
        self._maxusage = maxusage
        self._setsession = setsession
        self._closeable = closeable
        self._args, self._kwargs = args, kwargs
        self.thread = (threadlocal or local)()

    def steady_connection(self):
        """Get a steady, non-persistent PyGreSQL connection."""
        return SteadyPgConnection(
            self._maxusage, self._setsession, self._closeable,
            *self._args, **self._kwargs)

    def connection(self):
        """Get a steady, persistent PyGreSQL connection."""
        try:
            con = self.thread.connection
        except AttributeError:
            con = self.steady_connection()
            self.thread.connection = con
        return con
