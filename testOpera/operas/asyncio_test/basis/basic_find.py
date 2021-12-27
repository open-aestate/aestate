import asyncio

from aestate.util.Log import logging
from testOpera.table.demoModels import Demo

# import pandas
demo = Demo()
log = logging.gen(demo)
r1 = demo.find_one_async("SELECT * FROM demo WHERE id=%s", params=[1])
r2 = demo.find_sql_async("SELECT * FROM demo WHERE id>%s", params=[0])
r3 = demo.orm.find().where(name__love='a').end_async()
r1 = asyncio.run(r1)
r2 = asyncio.run(r2)
r3 = asyncio.run(r3)
log.error('r1', type(r1), r1)
log.error('r2', type(r2), r2)
log.error('r3', type(r3), r3)
