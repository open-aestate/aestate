import asyncio

from testOpera.table.demoModels import Demo

demo = Demo()
r = demo.find_one("SELECT * FROM demo order by `id` desc limit 1")
r1 = r.remove_async()
print('r1', asyncio.run(r1))
# del r
