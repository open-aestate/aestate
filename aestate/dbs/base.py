from typing import Tuple

from aestate.work.Manage import Pojo


class OperaBase:
    def __init__(self, instance: Pojo):
        self.instance = instance
        self.R = None

    def extra(self, field) -> Tuple[bool, object]: ...

    def check(self): ...

    def create(self): ...
