from CACodeFramework.field.sql_fields import *


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

    def parse_key(self, is_field=True, *args):
        """
        解析键格式,如:
            INSERT INTO `demo` (这里的就是键) VALUES ('','','','');
        :param is_field:是否格式化成 `%s` 格式
        :param args:
        :return:
        """
        if args is not None and len(args) != 0:
            self.args = args

        fields = parse_main(*self.args, to_str=True, is_field=is_field)
        return fields

    def parse_value(self, *args, to_str=False):
        """
        解析值格式,如:
            INSERT INTO `demo` (`index`, `title`, `selects`, `success`) VALUES (这里的就是值);
        :param args:
        :param to_str:
        :return:
        """
        if args is not None:
            self.args = args
        if to_str is not None:
            self.to_str = to_str
        values = parse_main(*self.args, to_str=self.to_str)
        return values

    def parse_insert(self, keys, values, __table_name__):
        fields = self.parse_key(*keys)
        values = self.parse_value(*values)
        # 分析需要几个隐藏值
        hides_value = ''
        for i in range(len(values)):
            hides_value += '%s,'
        # 去除末尾的逗号
        hides_value = hides_value[0: len(hides_value) - 1]
        str(values)
        sql = '%s`%s` (%s)%s(%s)' % (
            insert_str,
            str(__table_name__), fields, values_str, hides_value
        )

        kes = {'sql': sql}
        args = []
        for i in values:
            args.append(i)
        kes['params'] = args
        return kes
