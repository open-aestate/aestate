# -*- utf-8 -*-
import time

from aestate.util.Log import logging
from aestate.work.Cache import SqlCacheManage, CacheStatus
from testOpera.table.demoModels import ReadXmlClass

rxc = ReadXmlClass()
log = logging.gen(rxc)
scm = SqlCacheManage()


def find():
    s_time = time.time()
    start_time = time.time()
    for i in range(100):
        rxc.findInDemo(id=i)
        if i == 5:
            SqlCacheManage.status = CacheStatus.OPEN
        log.warn('execute:', time.time() - start_time)
        start_time = time.time()
    log.warn('using:', time.time() - s_time)
    log.info('get_size:', scm.get_size())
    log.info('get_capacity_max:', scm.get_capacity_max())
    log.info('get_max:', scm.get_max())
    rxc.insertTest(name='a', password="b")
    log.warn('using:', time.time() - s_time)
    log.info('get_size:', scm.get_size())
    log.info('get_capacity_max:', scm.get_capacity_max())
    log.info('get_max:', scm.get_max())


find()
find()
log.info('size:', scm.get_size())
find()
