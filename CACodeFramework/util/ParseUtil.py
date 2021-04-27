import copy

from CACodeFramework.pojoManager import tag


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

    def parse_insert(self, keys, values, __table_name__, insert_str, values_str):
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
    def parse_insert_pojo(pojo, __table_name__, insert_str, values_str):
        """
        解析插入语句

        INSERT INTO `__table_name__`(`title`,'selects') VALUE ('','')

        :param pojo:POJO对象
        :param __table_name__:表名
        :param insert_str:insert的sql方言
        :param values_str:values的sql方言
        :return:
        """
        _dict = pojo.fields
        # 得到所有的键
        keys = pojo.fields
        # 在得到值之后解析是否为空并删除为空的值和对应的字段
        cp_value = []
        # 复制新的一张字段信息
        keys_copy = []

        values = [getattr(pojo, v) for v in keys]
        for i, j in enumerate(values):
            if j is not None and not ParseUtil.is_default(j):
                keys_copy.append(keys[i])
                cp_value.append(j)
        return ParseUtil().parse_insert(keys_copy, cp_value, __table_name__, insert_str=insert_str,
                                        values_str=values_str)

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

    @staticmethod
    def last_id(**kwargs):
        """作者:CACode 最后编辑于2021/4/12

        遵循规则：

            内部>配置文件

        是否包含返回最后一行ID的配置

        只存在于更新操做的方法内，如：

            insert,

            update,

            delete

         Attributes:

             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'last_id' not in kwargs.keys():
            c_dict = conf_obj.get_dict()
            if 'last_id' in c_dict.keys():
                kwargs['last_id'] = c_dict['last_id']
            else:
                kwargs['last_id'] = False
        return kwargs

    @staticmethod
    def print_sql(**kwargs):
        """
        遵循规则：
            内部>配置文件

        是否包含打印sql的配置

        存在于所有数据库操做

        Attributes:
             conf_obj:配置类
        """
        conf_obj = kwargs['config_obj']
        if 'print_sql' not in kwargs.keys():
            c_dict = conf_obj.get_dict()
            if 'print_sql' in c_dict.keys():
                kwargs['print_sql'] = c_dict['print_sql']
            else:
                kwargs['print_sql'] = False
        return kwargs

    @staticmethod
    def case_name(text, rep_text='_', lower=True, upper=False):
        """
        将驼峰文本改为使用指定符号分割的字符串表达形式并全部小写
        :param text:需要替换的文本
        :param rep_text:在大写文本后面追加的字符串
        :param lower:是否需要全部小写
        :param upper:是否需要全部大写
        """
        lst = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                lst.append(rep_text)
            lst.append(char)

        if lower:
            return "".join(lst).lower()
        elif upper:
            return "".join(lst).upper()
        else:
            return "".join(lst)

    @staticmethod
    def is_default(__val):
        """
        是否等于默认值
        """
        try:
            t_v = __val.__class__.__bases__
            t_bf = tag.baseTag
            return t_v[len(t_v) - 1] == t_bf
        except SyntaxError:
            return False

    @staticmethod
    def set_field(obj, key, value):
        """
        当对象没有这个字段时，为对象设置一个字段

        为了方便提高拓展性可解耦，框架内部务必使用此

        方法或者set_field_compulsory()为操作管理类提供对象

        """
        if not hasattr(obj, key):
            setattr(obj, key, value)

    @staticmethod
    def set_field_compulsory(obj, key, value):
        """
        强制为一个对象设置一个字段并赋值

        此方法使用会覆盖原有的字段内容，强制使用覆盖字段时请先结合已有字段值判断是否真正需要覆盖操作

        """
        setattr(obj, key, value)
