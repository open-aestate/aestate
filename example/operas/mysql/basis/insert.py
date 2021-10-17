from example.table.demoModels import Demo

demo = Demo()
r1 = demo.create(Demo(name="test", password="test"))
demo.name = "test"
demo.password = "test"
r2 = demo.save()
data = {
    'name': 'test',
    'password': 'test'
}
r3 = demo.copy(**data).save()

print("r1", r1)
print("r2", r2)
print("r3", r3)
