from example.tables.demoModels import Demo, ReadXmlClass

demo = Demo()

r1 = demo.find_all_where_id(id=1, name="asdasd")
r2 = demo.find_all_F_where_id_eq_and_name_eq(id=1, name="asdasd")
r3 = demo.find_all_F_where_id_in_and_name_like_order_by_id(id=[1, 2, 3, 4], name="%a%")
print('r1', type(r1), r1)
print('r2', type(r2), r2)
print('r3', type(r3), r3)
r = ReadXmlClass()
r4 = r.findAllById()
r5 = r.findAllByIdName()
print('r4', type(r4), r4)
print('r5', type(r5), r5)
