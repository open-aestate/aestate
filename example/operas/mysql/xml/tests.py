# -*- utf-8 -*-
from aestate.ajson import aj
from example.table.demoModels import ReadXmlClass

rxc = ReadXmlClass()
r1 = rxc.findAllById(id=18)
r2 = rxc.insertTest(name='a', password="b")
r3 = rxc.updateTest(name='a', password="b", id=1)
r4 = rxc.deleteTest(id=2)
print('r1:', r1)
print('r2:', aj.parse(r2, bf=True))
print('r3:', aj.parse(r3, bf=True))
print('r4:', aj.parse(r4, bf=True))
