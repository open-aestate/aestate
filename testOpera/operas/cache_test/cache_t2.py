# -*- utf-8 -*-
import time

from aestate.ajson import aj
from aestate.util.Log import logging
from aestate.work.Cache import SqlCacheManage, CacheStatus, SqlCacheItem
from testOpera.table.demoModels import ReadXmlClass

rxc = ReadXmlClass()
log = logging.gen(rxc)
a = rxc.findAllById(id=0)
print(aj.parse(a.to_dict(), bf=True))
scm = SqlCacheManage()
SqlCacheManage.status = CacheStatus.CLOSE
log.info('size:', scm.get_container().__sizeof__())
s_time = time.time()
start_time = time.time()
for i in range(100):
    log.warn(rxc.findAllById(id=i))
    if i == 19:
        SqlCacheManage.status = CacheStatus.OPEN
        log.warn(rxc.findAllById(id=i))
    log.warn(f'execute {i}:', time.time() - start_time)
    start_time = time.time()


def levelOrder(root):
    """
    :type root: TreeNode
    :rtype: List[List[int]]
    """
    nodeQuene = []
    result = []
    if not root:
        return result
    nodeQuene.append(root)
    while nodeQuene:
        # 这个表示单层节点所有的值
        singleLevel = []
        queneLength = len(nodeQuene)
        for i in range(0, queneLength):
            currentNode = nodeQuene.pop(0)
            if currentNode.lchild:
                nodeQuene.append(currentNode.lchild)
            if currentNode.rchild:
                nodeQuene.append(currentNode.rchild)
            singleLevel.append(id(currentNode))
        result.append(singleLevel)
    return result


root = scm.get_container().root
tree_view = levelOrder(root)
print(tree_view)

log.warn('using:', time.time() - s_time)
log.info('size:', scm.get_container_size())
scm.clear()
log.info('size:', scm.get_container_size())
