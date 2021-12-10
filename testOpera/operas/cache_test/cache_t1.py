# -*- utf-8 -*-
import threading

from aestate.util.Log import logging
from testOpera.table.demoModels import Demo, ReadXmlClass

rxc = ReadXmlClass()
log = logging.gen(rxc)


def a():
    # [print(_, Demo(name='a').to_json()) for _ in range(100)]
    [log.info(rxc.findAllById(id=_)) for _ in range(100)]


def b():
    # [print(_, Demo(password='b').to_json()) for _ in range(100)]
    [log.info(rxc.findAllById(id=_)) for _ in range(100)]


def c():
    # [print(_, Demo(name='c').to_json()) for _ in range(100)]
    [log.info(rxc.findAllById(id=_)) for _ in range(100)]


t0 = threading.Thread(target=a)
t0.start()
t1 = threading.Thread(target=b)
t1.start()
t2 = threading.Thread(target=c)
t2.start()
t0.join()
t1.join()
t2.join()
