# -*- utf-8 -*-
from aestate.util.Log import logging
from example.table.demoModels import Demo

log = logging.gen(Demo())
[log.info('test info') for _ in range(1000)]
[log.warn('test warn') for _ in range(1000)]
[log.error('test error') for _ in range(1000)]
