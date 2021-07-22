from example.tables.demoModels import Demo

demo = Demo()
r1 = demo.create(Demo(name="test", password="test"))
demo.name = "test"
demo.password = "test"
r2 = demo.save()
print("r1", r1)
print("r2", r2)
