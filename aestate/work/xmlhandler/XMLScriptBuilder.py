# -*- utf-8 -*-
from abc import ABC


class NodeHandler(ABC):
    """节点事件抽象"""

    # 操作
    def handleNode(self): ...


class BindHandler(NodeHandler):
    def handleNode(self):
        pass
