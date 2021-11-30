# -*- utf-8 -*-
import time

import pymysql

from aestate.util.Log import logging
from aestate.work.Cache import SqlCacheManage, CacheStatus
from testOpera.table.demoModels import ReadXmlClass

rxc = ReadXmlClass()
log = logging.gen(rxc)
scm = SqlCacheManage()
SqlCacheManage.status = CacheStatus.CLOSE
log.info('size:', scm.get_container().__sizeof__())
s_time = time.time()
start_time = time.time()
for i in range(10):
    rxc.findAllById(id=10)
    if i == 5:
        SqlCacheManage.status = CacheStatus.OPEN
    log.warn('execute:', time.time() - start_time)
    start_time = time.time()
log.warn('using:', time.time() - s_time)
log.info('size:', scm.get_container().__sizeof__())
scm.clear()
log.info('size:', scm.get_container().__sizeof__())
