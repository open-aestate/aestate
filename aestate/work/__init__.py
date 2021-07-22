import threading

from aestate.cacode import Modes
from aestate.work.commad import __logo__


class Banner:
    _instance_lock = threading.Lock()

    def __init__(self, status: bool = False):
        self.status = status

    @classmethod
    def show(cls):
        Modes.Singleton.println(cls, __logo__)
