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

log.warn('using:', time.time() - s_time)
log.info('size:', scm.get_container_size())
scm.clear()
log.info('size:', scm.get_container_size())
