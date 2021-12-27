import asyncio

from aestate.work.Modes import EX_MODEL
from testOpera.table.demoModels import Demo

demo = Demo()
[demo.copy(name='test', password='test').save() for _ in range(10)]
r1 = demo.create_async(Demo(name="test", password="test"))
demo.name = "test"
demo.password = "test"
r2 = demo.save_async()
data = {
    'name': 'test',
    'password': 'test'
}
r3 = demo.copy(**data).save_async()
r4 = demo.execute_sql_async("INSERT INTO `demo`.`demo` ( `name`, `password`, `create_time`, `update_time`) "
                            "VALUES ( 'asdasd', 'aaa', '2021-05-28 00:08:22', '2021-07-24 02:40:38')",
                            mode=EX_MODEL.UPDATE)
print("r1", asyncio.run(r1))
print("r2", asyncio.run(r2))
print("r3", asyncio.run(r3))
print('r4', asyncio.run(r4))
