from testOpera.table.demoModels import Demo

demo = Demo()
r = demo.find_one("SELECT * FROM demo WHERE id=%s", params=[20])
r.name = "asdasd"
r1 = r.update()
print('r1', r1)
