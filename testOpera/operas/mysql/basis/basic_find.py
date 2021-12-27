from aestate.util.Log import logging
from testOpera.table.demoModels import Demo

demo = Demo()
log = logging.gen(demo)
r1 = demo.find_all(print_sql=False)
r1[0].name = "aaaaa"
r1[0].update()
r2 = demo.find_many("SELECT * FROM demo")
r3 = demo.find_field("id", "name", "password")
r4 = demo.find_one("SELECT * FROM demo WHERE id=%s", params=[1])
r5 = demo.find_sql("SELECT * FROM demo WHERE id>%s", params=[0])
r6 = demo.orm.find().where(name__love='a').end()
log.error('r1', type(r1), r1)
log.error('r2', type(r2), r2)
log.error('r3', type(r3), r3)
log.error('r4', type(r4), r4)
log.error('r5', type(r5), r5)
log.error('r6', type(r6), r6)
