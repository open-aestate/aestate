from example.table.demoModels import Demo

demo = Demo()
r = demo.find_one("SELECT * FROM demo order by `id` desc limit 1")
r1 = r.remove()
print('r1', r1)
# del r
