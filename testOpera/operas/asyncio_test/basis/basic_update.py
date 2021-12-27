import asyncio
import random

from testOpera.table.demoModels import Demo

c = 'qwertyuiopasdfghjklzcvbnm'
demo = Demo()
r = demo.find_one("SELECT * FROM demo order by `id` limit 1")

t = ''.join([c[random.randint(0, 25)] for a in range(random.randint(10, 20))])
print(t)
r.name = t
r1 = r.update_async()
print('r1', asyncio.run(r1))
