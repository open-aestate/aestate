from aestate.util.Log import logging
from testOpera.table.demoModels import Demo, ReadXmlClass

demo = Demo()
log = logging.gen(demo)
r1 = demo.find_all_where_id(id=1, name="asdasd")
rr1 = demo.find_all_where_id(id=1, name="asdasd")
r2 = demo.find_all_F_where_id_eq_and_name_eq(id=1, name="asdasd")
r3 = demo.find_all_F_where_id_in_and_name_like_order_by_id(id=[1, 2, 3, 4], name="%a%")
r4 = demo.find_all_F()
c = ReadXmlClass()
c1 = c.findAllById(id=10)
log.info('r1', type(r1), r1)
log.info('rr1', type(rr1), rr1)
log.info('r2', type(r2), r2)
log.info('r3', type(r3), r3)
log.info('r4', type(r4), r4)
log.info('c1', type(c1), c1)
