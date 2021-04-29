# 所有常量以空格开头并且以空格结束
# 空格符
space = ' '


def parse_field(key: str) -> str:
    return space + key + space


# 角标
subscript = '`'
# 插入
insert_str = parse_field('INSERT INTO')
# 删除
delete_str = parse_field('DELETE')
# 修改
update_str = parse_field('UPDATE')
# 查找
find_str = parse_field('SELECT')
# 当
where_str = parse_field('WHERE')
# 根据
by_str = parse_field('BY')
# 根据排序
order_by_str = parse_field('ORDER BY')
# 根据
group_by_str = parse_field('GROUP BY')
# 倒叙
desc_str = parse_field('DESC')
# 设置
set_str = parse_field('SET')
# 和
ander_str = parse_field('AND')
# 分页
limit_str = parse_field('LIMIT')
# 从
from_str = parse_field('FROM')
# 值
value_str = parse_field('VALUE')
# 多个值
values_str = parse_field('VALUES')
# as
asses_str = parse_field('as')
# 运算符
symbol = '>> << == <= >= != - + / * %'.split(' ')
left_par = parse_field('(')
right_par = parse_field(')')
comma = parse_field(',')
eq = parse_field('=')


def parse_set(keys):
    """
    格式化set键
    """
    keys_str = ''
    for i in keys:
        keys_str += '{}=%s{}'.format(i, ander_str)
    keys_str = keys_str[0:len(keys_str) - len(ander_str)]
    return keys_str
