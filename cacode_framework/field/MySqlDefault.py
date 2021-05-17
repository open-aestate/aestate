# 所有常量以空格开头并且以空格结束
# 空格符
import threading

from ..cacode.Modes import Singleton


class MySqlFields_Default:
    """
    默认的数据库方言配置
    """

    _instance_lock = threading.RLock()

    @staticmethod
    def parse_field(key: str) -> str:
        return f' {key} '

    @property
    def left_subscript(self):
        """
        左角标
        """
        return '`'

    @property
    def space(self):
        """
        空格
        """
        return ' '

    @property
    def right_subscript(self):
        """
        右角标
        """
        return '`'

    @property
    def insert_str(self):
        """
        插入
        """
        return self.parse_field('INSERT INTO')

    @property
    def delete_str(self):
        """
        删除
        """
        return self.parse_field('DELETE')

    @property
    def update_str(self):
        """
        更新
        """
        return self.parse_field('UPDATE')

    @property
    def find_str(self):
        return self.parse_field('SELECT')

    @property
    def where_str(self):
        return self.parse_field('WHERE')

    @property
    def by_str(self):
        return self.parse_field('BY')

    @property
    def order_by_str(self):
        return self.parse_field('ORDER BY')

    @property
    def group_by_str(self):
        return self.parse_field('GROUP BY')

    @property
    def desc_str(self):
        return self.parse_field('DESC')

    @property
    def set_str(self):
        return self.parse_field('SET')

    @property
    def ander_str(self):
        return self.parse_field('AND')

    @property
    def limit_str(self):
        return self.parse_field('LIMIT')

    @property
    def from_str(self):
        return self.parse_field('FROM')

    @property
    def value_str(self):
        return self.parse_field('VALUE')

    @property
    def values_str(self):
        return self.parse_field('VALUES')

    @property
    def asses_str(self):
        return self.parse_field('AS')

    @property
    def left_par(self):
        return self.parse_field('(')

    @property
    def right_par(self):
        return self.parse_field(')')

    @property
    def comma(self):
        return self.parse_field(',')

    @property
    def eq(self):
        return self.parse_field('=')

    @property
    def symbol(self):
        return '>> << == <= >= != - + / * %'.split(' ')

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
