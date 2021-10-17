from example.config.demoModels import Demo
import pandas

demo = Demo()
r1 = demo.find_all()
r2 = demo.find_many("SELECT * FROM demo")
r3 = demo.find_field("id", "name", "password")
r4 = demo.find_one("SELECT * FROM demo WHERE id=%s", params=[1])
r5 = demo.find_sql("SELECT * FROM demo WHERE id>%s", params=[0])
print('r1', type(r1), r1)
print('r2', type(r2), r2)
print('r3', type(r3), r3)
print('r4', type(r4), r4)
print('r5', type(r5), r5)

df = pandas.DataFrame.from_dict(r1.to_dict())
print(df)
