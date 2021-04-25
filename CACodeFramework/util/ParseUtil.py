import copy

from CACodeFramework.field.sql_fields import *


# from CACodeFramework.pojoManager.Manage import Pojo


def parse_main(*args, to_str=False, is_field=False):
    """
        解析属性:
            将属性格式设置为:['`a`,','`b`,','`c`']
        :param to_str:是否转成str格式
        :param args:参数
        :param is_field:是否为表字段格式
        :return:
    """
    fields = []
    for value in args:
        if to_str:
            if is_field:
                fields.append('`%s`,' % (str(value)))
            else:
                fields.append('%s,' % (str(value)))
        else:
            fields.append(value)
    if len(fields) != 0:
        fields[len(fields) - 1] = fields[len(fields) - 1].replace(',', '')
        field_str = ''
        if to_str:
            for field in fields:
                field_str += field
            return field_str
        return fields
    else:
        return None


class ParseUtil(object):

    def __init__(self, *args, to_str=False, is_field=False):
        """
        初始化解析参数工具
        :param args:需要解析的参数
        :param to_str:是否转成str格式
        :param is_field:是否为表字段格式
        """
        self.args = args
        self.to_str = to_str
        self.is_field = is_field

    def parse_key(self, *args, **kwargs):
        """
        解析键格式,如:
            INSERT INTO `demo` (这里的就是键) VALUES ('','','','');
        :param args:
        :return:
        """
        if args is not None and len(args) != 0:
            self.args = args
        if 'is_field' in kwargs.keys():
            self.is_field = kwargs['is_field']

        fields = parse_main(*self.args, to_str=True, is_field=self.is_field)
        return fields

    def parse_value(self, *args, **kwargs):
        """
        解析值格式,如:
            INSERT INTO `demo` (`index`, `title`, `selects`, `success`) VALUES (这里的就是值);
        :param args:
        :return:
        """
        if args is not None and len(args) != 0:
            self.args = args
        if 'to_str' in kwargs.keys():
            self.to_str = kwargs['to_str']
        values = parse_main(*self.args, to_str=self.to_str)
        return values

    def parse_insert(self, keys, values, __table_name__):
        """
        解析成insert语句
        """
        # 转换键值对
        # 1.1.0.05更新
        # 本次修改无法解析键值对问题
        self.is_field = True
        fields = self.parse_key(*keys)
        self.to_str = False
        values = self.parse_value(*values)
        # 分析需要几个隐藏值
        hides_value = ['%s,' for i in range(len(values))]
        # for i in range(len(values)):
        #     hides_value += '%s,'
        # 去除末尾的逗号
        end = hides_value[len(hides_value) - 1]
        hides_value[len(hides_value) - 1] = end[0: len(end) - 1]
        # 得到最后隐藏符号的字符串表达格式
        value = ''.join(hides_value)
        sql = '%s`%s` (%s)%s(%s)' % (
            insert_str,
            str(__table_name__), fields, values_str, value
        )

        kes = {'sql': sql}
        args = []
        for i in values:
            args.append(i)
        kes['params'] = args
        return kes

    @staticmethod
    def parse_obj(data: dict, instance: object) -> object:
        """
                将数据解析成对象
                注意事项:
                    数据来源必须是DbUtil下查询出来的
                :param data:单行数据
                :param instance:参与解析的对象
                :return:POJO对象
                """
        # 深度复制对象
        part_obj = copy.copy(instance)
        for key, value in data.items():
            setattr(part_obj, key, value)
        return part_obj
