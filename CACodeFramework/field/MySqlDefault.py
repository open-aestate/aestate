# 所有常量以空格开头并且以空格结束
# 空格符
import threading

from CACodeFramework.cacode.Modes import Singleton

space = ' '


def parse_field(key: str) -> str:
    return space + key + space


class MySqlFields_Default:
    """
    默认的数据库方言配置
    """

    _instance_lock = threading.RLock()

    def __init__(self):
        # 角标
        self.subscript = '`'
        # 插入
        self.insert_str = parse_field('INSERT INTO')
        # 删除
        self.delete_str = parse_field('DELETE')
        # 修改
        self.update_str = parse_field('UPDATE')
        # 查找
        self.find_str = parse_field('SELECT')
        # 当
        self.where_str = parse_field('WHERE')
        # 根据
        self.by_str = parse_field('BY')
        # 根据排序
        self.order_by_str = parse_field('ORDER BY')
        # 根据
        self.group_by_str = parse_field('GROUP BY')
        # 倒叙
        self.desc_str = parse_field('DESC')
        # 设置
        self.set_str = parse_field('SET')
        # 和
        self.ander_str = parse_field('AND')
        # 分页
        self.limit_str = parse_field('LIMIT')
        # 从
        self.from_str = parse_field('FROM')
        # 值
        self.value_str = parse_field('VALUE')
        # 多个值
        self.values_str = parse_field('VALUES')
        # as
        self.asses_str = parse_field('as')
        # 运算符
        self.symbol = '>> << == <= >= != - + / * %'.split(' ')
        self.left_par = parse_field('(')
        self.right_par = parse_field(')')
        self.comma = parse_field(',')
        self.eq = parse_field('=')
        self.space = " "

    def parse_set(self, keys):
        """
        格式化set键
        """
        keys_str = ''
        for i in keys:
            keys_str += '{}=%s{}'.format(i, self.ander_str)
        keys_str = keys_str[0:len(keys_str) - len(self.ander_str)]
        return keys_str

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createDbOpera(cls)
        return instance
