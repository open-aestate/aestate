# 所有常量以空格开头并且以空格结束
# 空格符
space = ' '
# 角标
subscript = '`'
# 插入
insert_str = space + 'INSERT INTO' + space
# 删除
delete_str = space + 'DELETE' + space
# 修改
update_str = space + 'UPDATE' + space
# 查找
find_str = space + 'SELECT' + space
# 当
where_str = space + 'WHERE' + space
# 根据
by_str = space + 'BY' + space
# 根据排序
order_by_str = space + 'ORDER BY' + space
# 倒叙
desc_str = space + 'DESC' + space
# 设置
set_str = space + 'SET' + space
# 和
ander_str = space + 'AND' + space
# 分页
limit_str = space + 'LIMIT' + space
# 从
from_str = space + 'FROM' + space
# 值
value_str = space + 'VALUE' + space
# 多个值
values_str = space + 'VALUES' + space
# 运算符
symbol = '>> << == <= >= != - + / * %'.split(' ')
left_par = space + '(' + space
right_par = ')'
comma = ','
eq = '='


def parse_set(keys):
    """
    格式化set键
    """
    keys_str = ''
    for i in keys:
        keys_str += '{}=%s{}'.format(i, ander_str)
    keys_str = keys_str[0:len(keys_str) - len(ander_str)]
    return keys_str


if __name__ == '__main__':
    print(parse_set(['title', 'selects']))
