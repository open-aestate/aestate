from summer.exception import e_fields
from summer.util.Log import CACodeLog


class CACodePureORM(object):
    """
    纯净的ORM模式:
        你可以使用find('table').by('args').order_by('args').desc().end()方式执行sql
        好处就是:
            能更好的拒绝sql注入
            无需写sql语句
            代码简单易懂
            上手快
    """

    def __init__(self, repository):
        """
        初始化ORM


        自定义方言除了可使用默认已存在的方法，还可以使用自定义sql方言拼接

        :param repository:仓库
s        """
        self.args = []
        self.params = []
        self.sqlFields = None
        # self.sqlFields = sqlFields
        self.ParseUtil = repository.config_obj
        self.serializer = repository.serializer
        self.sqlFields = repository.sqlFields
        # 创建sql语法
        if repository is None:
            CACodeLog.err(
                AttributeError, 'Repository is null,Place use repository of ORM framework')
        self.repository = repository
        self.__table_name__ = '{}{}{}'.format(self.sqlFields.left_subscript, repository.__table_name__,
                                              self.sqlFields.right_subscript)

        self.first_data = False

    def top(self):
        return self.find().limit(1)

    def first(self):
        """
        是否只返回第一行数据
        """
        self.first_data = True
        return self

    # ------------------------主键--------------------------

    def insert(self, pojo):
        """
        插入
        example:
            insert()
            insert('c1','c2')
        :param pojo:需要插入的对象
        """
        # 添加insert关键字
        # self.args.append(insert_str)
        # self.args.append('{}{}'.format(self.__table_name__, left_par))
        sql = self.ParseUtil.parse_insert_pojo(
            pojo, self.__table_name__.replace('`', ''), insert_str=self.sqlFields.insert_str,
            values_str=self.sqlFields.values_str)
        self.args.append(sql['sql'])
        self.params = sql['params']

        # _dict = pojo.__dict__
        # keys = []
        # # 解析item
        # for key, value in _dict.items():
        #     # 去除为空的键
        #     if value is None:
        #         continue
        #     keys.append('`{}`{}'.format(key, comma))
        #     self.params.append(value)
        # for i in keys:
        #     self.args.append(i)
        # # 将最后一个字段的逗号改成空格
        # self.rep_sym(comma, space)
        # # 加上右边括号
        # self.args.append(right_par)
        # self.args.append('{}{}'.format(values_str, left_par))
        # for i in keys:
        #     self.args.append('%s{}'.format(comma))
        # # 将最后一个字段的逗号改成空格
        # self.rep_sym(comma, space)
        # self.args.append(right_par)
        return self

    def delete(self):
        """
        删除
        """
        self.args.append(self.sqlFields.delete_str)
        self.args.append(self.sqlFields.from_str)
        self.args.append(self.__table_name__)
        return self

    def update(self):
        """
        更新
        example:
            update().set(key=value).where(key1=value1)
        """
        update_sql = '%s%s' % (self.sqlFields.update_str,
                               str(self.__table_name__))
        self.args.append(update_sql)
        return self

    def find(self, *args, **kwargs):
        """
        查
        example:
            find('all')
            find('param1',asses=['p'],h_func=True)
        Attributes:
            asses:将对应的字段转成另一个别名,不需要转换的使用None标识
            h_func:不将字段转换成 `%s` 格式
        更新:
            如果args字段长度为0,默认为查找全部
        """
        self.args.append(self.sqlFields.find_str)
        # 如果有as字段
        asses = None
        if 'asses' in kwargs.keys():
            asses = kwargs['asses']
        # 如果包含方法的字段，则不加密
        func_flag = False
        if 'h_func' in kwargs.keys():
            func_flag = kwargs['h_func']
        # 1.1.0.05更新,默认为all
        _all = False
        if len(args) == 0:
            _all = True
        # 如果存在all
        # 1.1.1.2修复：tuple index out of range
        if _all or 'all'.upper() == args[0].upper():
            # 如果包含all关键字,则使用解析工具解析成字段参数
            if not func_flag:
                fields = self.ParseUtil.parse_key(*self.repository.fields, is_field=True)
            else:
                fields = self.ParseUtil.parse_key(*self.repository.fields, is_field=False)
        else:
            if not func_flag:
                fields = self.ParseUtil.parse_key(*args, is_field=True)
            else:
                fields = self.ParseUtil.parse_key(*args)
        # 解决as问题
        if asses is not None:
            fs = fields.split(',')
            if len(fs) != len(asses):
                # 匿名参数长度与字段长度不符合
                raise TypeError(
                    'The length of the anonymous parameter does not match the length of the field')
            for i, v in enumerate(fs):
                if asses[i] is not None:
                    self.args.append('{}{}{}'.format(
                        v, self.sqlFields.asses_str, asses[i]))
                else:
                    self.args.append(v)
                # 逗号
                self.args.append(self.sqlFields.comma)
        else:
            self.args.append(fields)
        if asses is not None:
            # 去掉末尾的逗号
            self.rep_sym()
        #     加上from关键字
        if 'poly' not in kwargs.keys():
            self.con_from()
        else:
            self.args += kwargs['poly']
        return self

    def order_by(self, *args):
        """
        根据什么查
        example:
            find('all').order_by('param')
            find('all').order_by('param').end()
            find('all').order_by('p1','p2').desc().limit(10,20)
        """
        return self.by_opera(field=self.sqlFields.order_by_str, args_list=args)

    def group_by(self, *args):
        """
        聚合函数
        example:
            select shop_id,count(*) as count from comments group by shop_id having count>1;
        """
        return self.by_opera(field=self.sqlFields.group_by_str, args_list=args)

    def by_opera(self, field, args_list):
        """
        根据什么查
        """
        self.args.append(field)
        for i in args_list:
            self.args.append(self.sqlFields.left_subscript)
            self.args.append(i)
            self.args.append(self.sqlFields.right_subscript)
            self.args.append(self.sqlFields.ander_str)
        self.rep_sym(self.sqlFields.ander_str, self.sqlFields.space)
        return self

    def where(self, **kwargs):
        """
        当....
        example:
            find('ALL').where(param='%s') - 默认符号为等于 ==
            find('ALL').where(param='==%s')
            find('ALL').where(param='>%d')
            find('ALL').where(param='<%d')
            find('ALL').where(param='<=%d')
            find('ALL').where(param='>=%.2f')
            find('ALL').where(param='!=%.2f')
        复杂语法:
            find('ALL').where(param='+%d/%d==%d')
            find('ALL').where(param='-%.2f*%d==12')
            find('ALL').where(param='*10-1==12')
            find('ALL').where(param='/10+1==12')
        """
        self.args.append(self.sqlFields.where_str)
        for key, value in kwargs.items():
            cp_key = key
            customize = False
            sym = '='
            if len(str(value)) > 2 and str(value)[0:2] in self.sqlFields.symbol:
                sym = value[0:2]
                value = str(value)[2:len(str(value))]
            elif sym == '==':
                sym = '='
            elif sym == '>>':
                sym = '>'
            elif sym == '<<':
                sym = '<'
            else:
                # 没有找到符号的话就从字段名开始
                # 截取最后一段从两段下划线开始的末尾
                sps = cp_key.split('__')
                if not len(sps) == 1:
                    customize = True
                    sym = sps[len(sps) - 1]
                    self.ParseUtil.fieldExist(self.ParseUtil, 'adapter', raise_exception=True)
                    cp_key = cp_key[:cp_key.rfind('__' + sym)]
                    self.ParseUtil.adapter.funcs[sym](self, cp_key, value)

            if not customize:
                self.args.append('`{}`{}%s'.format(cp_key, sym))
                self.args.append(self.sqlFields.ander_str)
                self.params.append(value)
        self.rep_sym(self.sqlFields.ander_str)

        return self

    def limit(self, star=0, end=None):
        """
        分页
        :param star:开始
        :param end:末尾
        example:
            find('all').limit(star=10,end=20)
            find('all').limit(end=10)
        """
        self.args.append(self.sqlFields.limit_str)
        # 死亡空格
        if end is None:
            limit_param = '{}{}{}'.format(
                self.sqlFields.space, star, self.sqlFields.space)
        else:
            limit_param = '{}{}{}{}{}'.format(self.sqlFields.space, star, self.sqlFields.comma, end,
                                              self.sqlFields.space)
        self.args.append(limit_param)
        return self

    def desc(self):
        """
        倒叙
        example:
            find('all').desc()
            find('all').desc().end()
            find('all').order_by('param').desc().limit(10,20)
        """

        if self.sqlFields.order_by_str not in self.args:
            CACodeLog.err(AttributeError,
                          e_fields.CACode_SqlError('There is no `order by` field before calling `desc` field,'
                                                   'You have an error in your SQL syntax'))

        self.args.append(self.sqlFields.desc_str)
        return self

    def set(self, **kwargs):
        """
        设置
        example:
            update('table').set('param','value').end()
            update('table').set('param1','value1').where('param2=value2').end()
        """
        self.args.append(self.sqlFields.set_str)
        _size = len(kwargs.keys())
        for key, value in kwargs.items():
            self.args.append('`{}`{}%s'.format(key, self.sqlFields.eq))
            # set是加逗号不是and
            self.args.append(self.sqlFields.comma)
            self.params.append(value)
        self.rep_sym(self.sqlFields.comma)
        return self

    # ------------------------预设符--------------------------

    def ander(self):
        """
        和
        example:
            update('table').set('param1','value1').and().set('param2','value2')
            update('table').set('param1','value1').and().set('param2','value2').end()
            update('table').set('param1','value1').and().set('param2','value2').where('param3=value3').end()
        """
        self.args.append(self.sqlFields.ander_str)
        return self

    def run(self, need_sql=False):
        """
        最终执行任务
        """
        sql = ''
        conf = self.ParseUtil.get_dict()
        print_sql = 'print_sql' in conf.keys() and conf['print_sql'] is True
        last_id = 'last_id' in conf.keys() and conf['last_id'] is True
        sql += ''.join(self.args)
        if need_sql:
            return sql
        if self.sqlFields.find_str in sql:
            _result = self.repository.db_util.select(
                sql=sql,
                params=self.params,
                print_sql=print_sql,
                last_id=last_id
            )
            _result_objs = []
            for i in _result:
                _obj = self.ParseUtil.parse_obj(
                    data=i, instance=self.repository.instance)
                _result_objs.append(_obj)
            _result = _result_objs
        else:
            _result = self.repository.db_util.update(
                sql=sql,
                params=self.params,
                print_sql=print_sql,
                last_id=last_id
            )
        # 清空资源，为下一次使用做准备
        self.args.clear()
        self.params.clear()
        if self.first_data:
            if type(_result) is list or type(_result) is tuple:
                return self.serializer(instance=self.repository.instance, base_data=_result).first()
        else:
            q = self.serializer(
                instance=self.repository.instance, base_data=_result)
            return q

    def con_from(self):
        """
        如果没有被from包含,则在末尾加上from __table_name__关键字
        """
        if self.sqlFields.from_str not in self.args:
            self.args.append(self.sqlFields.from_str)
            # 然后加上表名
            self.args.append(self.__table_name__)

    def append(self, app_sql):
        """
        末尾追加一些sql
        """
        self.args.append(app_sql)
        return self

    def rep_sym(self, sym=',', rep=''):
        """
        将最后一个参数包含的指定字符替换为指定字符
        """
        self.args[len(self.args) -
                  1] = str(self.args[len(self.args) - 1]).replace(sym, rep)
        return self

    def end(self):
        return self.run()

    def __rshift__(self, other):
        """
        将左边orm迁移至右边
        """
        new_args = self.args.copy()
        new_args.append(' ) ')
        other.args.append(' ( ')
        other.args += new_args
        return other

    def __lshift__(self, other):
        """
        将右边迁移至左边
        """
        new_args = other.args.copy()
        new_args.append(' ) ')
        self.args.append(' ( ')
        self.args = self.args + new_args
        return self
