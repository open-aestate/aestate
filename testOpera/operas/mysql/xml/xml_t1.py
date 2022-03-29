# -*- utf-8 -*-
from aestate.ajson import aj
from aestate.util.Log import logging
from testOpera.table.demoModels import ReadXmlClass

rxc = ReadXmlClass()
log = logging.gen(rxc)
a = rxc.findInDemo(id=3)
# r1 = rxc.findAllById(id=18)
# rr1 = rxc.findAllByIdDict(id=18)
# r2 = rxc.insertTest(name='a', password="b")
# r3 = rxc.updateTest(name='a', password="b", id=1)
# r4 = rxc.deleteTest(id=2)
# # log.info('\nr1:', r1.to_json(True))
# log.info('rr1:', rr1)
# log.info('r2:', aj.parse(r2, bf=True))
# log.info('r3:', aj.parse(r3, bf=True))
# log.info('r4:', aj.parse(r4, bf=True))

print(a.first().status)
print(a.to_json(True))
