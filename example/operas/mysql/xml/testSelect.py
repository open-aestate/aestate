# -*- utf-8 -*-
from aestate.ajson import aj
from example.table.demoModels import ReadXmlClass

rxc = ReadXmlClass()
r1 = rxc.findAllById(id=18)
print('select result:', aj.parse(r1, bf=True))
