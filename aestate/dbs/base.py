from typing import Tuple


class OperaBase:
    def __init__(self, instance):
        self.instance = instance
        self.R = None

    def extra(self, field) -> Tuple[bool, object]: ...

    def check(self): ...

    def create(self): ...
