# -*- utf-8 -*-
from aestate.util.Log import logging
from example.table.demoModels import Demo

log = logging.gen(Demo())
[log.info(True, 'test info') for _ in range(10000)]
[log.warn(True, 'test warn') for _ in range(10000)]
[log.error(True, 'test error') for _ in range(10000)]