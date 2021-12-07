import copy

from aestate.work.Modes import EX_MODEL
from aestate.work.Serialize import QuerySet
from aestate.exception import FieldNotExist
from aestate.dbs import _mysql
from aestate.work.sql import ExecuteSql, ProxyOpera
from aestate.util.Log import ALog

from aestate.work.orm import AOrm

# 每个任务唯一ID
import uuid


class Repository:
    """
    - POJO类
        - 继承该类表名此类为数据库的pojo类
        - 需要配合:@Table(name, msg, **kwargs)使用
    """

    def __init__(self, config_obj=None, instance=None, log_conf=None, close_log=False, serializer=QuerySet, **kwargs):
        """
        通过继承此类将数据表实体化

            实体化之后你可以使用像类似find_one()等操做

            可以调用conversion()方法将其转化为ORM框架常用的样式

            无需担心类型问题，无需担心datetime无法转换
        使用方法:
            #加入Table注解，并标注表名与描述，因考虑使用者后期优化问题，请务必填写MSG参数

            @Table(name="demo_table", msg="demo message")

            #继承Repository并得到相对应的半自动ORM操做
            class TestClass(Repository):
                # 初始化并super配置
                def __init__(self,**kwargs):
                    super(DemoTable, self).__init__(config_obj=ConF(), log_conf={
                        'path': "/log/",
                        'save_flag': True
                    }, **kwargs)

        初始化配置:

            aestate.util.Config.config的配置类,详见:aestate.work.Config.MysqlConfig

        Attributes:
            以下的字段均可覆盖重写

            config_obj:数据源配置类

            log_conf:日志配置工具

            log_obj:日志对象

            close_log:是否关闭日志

            serializer:序列化使用的类,默认使用aestate.work.Serialize.QuerySet

            instance:实例

            __table_name__:表名称

            operation:操作类的实现

            fields:操作的字段

            sqlFields:sql方言

        :param config_obj:配置类
        :param log_conf:日志配置类
        :param close_log:是否关闭日志显示功能
        :param serializer:自定义序列化器,默认使用aestate.work.Serialize.QuerySet
        """
        # 以下使用ParseUtil将所有参数替换为可动态修改
        # 有没有关闭日志
        # 数据源配置
        if config_obj is None:
            ALog.log_error(msg="缺少配置类`config_obj`", obj=FieldNotExist, raise_exception=True)
        self.ParseUtil = config_obj
        ParseUtil = self.ParseUtil
        ParseUtil.set_field_compulsory(
            self, key='config_obj', data=kwargs, val=config_obj)
        # 抽象类
        ParseUtil.set_field_compulsory(
            obj=self, data=kwargs, key='abst', val=False)
        # 当本类为抽象类时，仅设置所需要的值
        ParseUtil.set_field_compulsory(
            self, key='close_log', data=kwargs, val=close_log)
        # 有没有表名
        ParseUtil.set_field_compulsory(self, key='__table_name__', data=kwargs,
                                       val=self.__table_name__ if hasattr(self, '__table_name__') else
                                       '"__table_name__" parsing failed')
        # 参照对象
        # 能操作数据库的，但是没有值
        ParseUtil.set_field_compulsory(
            self, key='instance', data=kwargs, val=instance)
        # 取得字段的名称
        ParseUtil.set_field_compulsory(
            self, key='fields', data=kwargs, val=list(self.instance.getFields().keys()))
        # 获取sql方言配置
        ParseUtil.set_field_compulsory(
            self, key='sqlFields', data=self.config_obj.__dict__, val=_mysql.Fields())
        # 当当前类为抽象类时，为类取消初始化数据库配置
        # 最后的执行结果
        ParseUtil.set_field_compulsory(
            self, key='result', data=kwargs, val=None)
        ParseUtil.set_field_compulsory(self, key='log_obj', data=kwargs,
                                       val=ALog(**log_conf) if log_conf is not None else None)
        if hasattr(self, 'close_log') and not self.close_log and not self.abst and not self.__init_pojo__:
            ALog.log(obj=self, msg='Being Initialize this object', LogObject=self.log_obj)
        ParseUtil.set_field_compulsory(
            self, key='serializer', data=kwargs, val=serializer)
        if not self.abst:
            # 操作类
            ParseUtil.set_field_compulsory(
                self, key='operation', data=kwargs, val=ProxyOpera.DbOperation())
            # 连接池
            if hasattr(self, 'config_obj') and self.config_obj:
                self.db_util = ExecuteSql.Db_opera(
                    creator=ParseUtil.fieldExist(
                        self.config_obj, 'creator', raise_exception=True),
                    POOL=None if 'POOL' not in kwargs.keys(
                    ) else kwargs['POOL'],
                    **ParseUtil.fieldExist(self.config_obj, 'kw', raise_exception=True))
            else:
                ALog.log_error('`config_obj` is missing', AttributeError, LogObject=self.log_obj, raise_exception=True)

    @property
    def conversion(self):
        """
        将此Repository转换为ORM实体

        Return:
            ORM转换之后的实体对象
        """
        return AOrm(repository=self)

    def first(self):
        """
        获取数据库中的第一个
        """
        return self.conversion.top().end()

    def last(self):
        """
        获取最后一个参数
        """
        return self.conversion.top().desc().end()

    def find_all(self, **kwargs) -> QuerySet:
        """
        从当前数据表格中查找所有数据

        Returns:
            将所有结果封装成POJO对象集合并返回数据
        """
        # 开启任务
        self.result = self.find_field(*self.getFields(), **kwargs)
        return self.result

    def find_field(self, *args, **kwargs) -> QuerySet:
        """
        只查询指定名称的字段,如:

            SELECT user_name FROM `user`

            即可参与仅解析user_name为主的POJO对象

        :param args:需要参与解析的字段名

        :return:
            将所有结果封装成POJO对象集合并返回数据

        """
        # 设置名称
        name = str(uuid.uuid1())
        # 开启任务
        kwargs.update(
            {
                'func': self.operation.__find_by_field__,
                '__task_uuid__': name,
                't_local': self
            }
        )

        result = self.operation.start(*args, **kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def find_one(self, sql, **kwargs):
        """
        查找第一条数据

            可以是一条

            也可以是很多条中的第一条

        code:

            result = self.find_many(**kwargs)
            if len(result) == 0:
                return None
            else:
                return result[0]

        :param kwargs:包含所有参数:

            pojo:参照对象

            sql:处理过并加上%s的sql语句

            params:需要填充的字段

            print_sql:是否打印sql语句

        :return 返回使用find_many()的结果种第一条
        """
        kwargs['sql'] = sql
        self.result = self.find_many(**kwargs)
        if self.result is None or len(self.result) == 0:
            self.result = []
            return None
        else:
            self.result = self.result.first()
            return self.result

    def find_many(self, sql, **kwargs) -> QuerySet:
        """
        查询出多行数据

            第一个必须放置sql语句

        :param kwargs:包含所有参数:

            pojo:参照对象

            sql:处理过并加上%s的sql语句

            params:需要填充的字段

            print_sql:是否打印sql语句

        :return 将所有数据封装成POJO对象并返回

        """
        # 设置名称
        name = str(uuid.uuid1())
        kwargs['sql'] = sql
        # 开启任务
        kwargs['func'] = self.operation.__find_many__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        result = self.operation.start(**kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def find_sql(self, sql, **kwargs) -> QuerySet:
        """

        返回多个数据并用list包装:

            - 可自动化操作

            - 请尽量使用find_many(sql)操作

        :param kwargs:包含所有参数:
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
            print_sql:是否打印sql语句
        """
        # kwargs['conf_obj'] = t_local.config_obj
        # 设置名称
        name = str(uuid.uuid1())
        kwargs['sql'] = sql
        # 开启任务
        kwargs['func'] = self.operation.__find_sql__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        result = self.operation.start(**kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def update(self, key=None):
        """
        执行更新操作:
            返回受影响行数

        :param key:主键，where的参考数据
        :return:
        """
        if key is None:
            for k, v in self._fields.items():
                if hasattr(v, "primary_key") and getattr(v, 'primary_key'):
                    key = k
                    break
        name = str(uuid.uuid1())
        kwargs = {
            'pojo': self,
            'func': self.operation.__update__,
            '__task_uuid__': name,
            't_local': self,
            'key': key
        }
        # 开启任务
        self.result = self.operation.start(**kwargs)
        return self.result

    def remove(self, key=None):
        """
        执行更新操作:
            返回受影响行数

        :param key:主键，where的参考数据
        :return:
        """
        if key is None:
            for k, v in self._fields.items():
                if hasattr(v, "primary_key") and getattr(v, 'primary_key'):
                    key = k
                    break
        name = str(uuid.uuid1())
        kwargs = {
            'pojo': self,
            'func': self.operation.__remove__,
            '__task_uuid__': name,
            't_local': self,
            'key': key
        }
        # 开启任务
        self.result = self.operation.start(**kwargs)
        return self.result

    def save(self, *args, **kwargs):
        """
        将当前储存的值存入数据库
        """
        kwargs['pojo'] = self
        return self.create(*args, **kwargs)

    def create(self, pojo, **kwargs):
        """
        插入属性:
            返回受影响行数
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
        :return:rowcount,last_id if last_id=True
        """
        # 设置名称
        kwargs['pojo'] = pojo
        name = str(uuid.uuid1())
        # 开启任务
        kwargs['func'] = self.operation.__insert__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        self.result = self.operation.start(**kwargs)
        return self.result

    def copy(self, **kwargs):
        """
        复制对象进行操做

        不建议多次创建对象，建议使用 pojo.copy()来生成对象
        """
        obj = copy.copy(self)
        [setattr(obj, k, v) for k, v in kwargs.items()]
        return obj

    def execute_sql(self, sql, params=None, mode=EX_MODEL.SELECT, **kwargs):
        """
        :param sql:执行的sql
        :param params:防止sql注入的参数
        :param mode:查询模式,默认使用SELECT,使用aestate.work.Modes.EX_MODEL枚举修改执行的sql类型
        :param kwargs:其他需要的参数
        """
        d = self.__dict__
        d.update(kwargs)
        kwargs = d
        kwargs['print_sql'] = False if 'print_sql' not in kwargs.keys() else kwargs['print_sql'] if kwargs[
            'print_sql'] else False
        if mode is None or mode == EX_MODEL.SELECT:
            return self.db_util.select(sql=sql, params=params, **kwargs)
        else:
            kwargs['last_id'] = True if 'last_id' not in kwargs.keys() else kwargs['last_id']
            return self.db_util.insert(sql=sql, params=params, **kwargs)

    def foreign_key(self, cls, key_name, field_name=None, data=None, operation=None):
        """
        根据外键来查

        Examples:
            第一种：

            >>> from apps.fontend.models import  Label, SmLabel
            >>> smlabel = SmLabel()
            >>> label = Label()
            >>> label.find_all()
            >>> label.foreign_key(smlabel.copy, 'label_id')
            >>> datas = label.datas

            第二种：

            >>> page = int(requests.GET['page']) \
            ...         if 'page' in requests.GET.keys() \
            ...         else 1
            ...
            >>> sm_label_list = sm_label.orm.filter(id=pk)
            >>> sm_label.foreign_key(
            ...    cls=need.copy,
            ...    key_name='label_id',
            ...    field_name="need_list",
            ...    datas=sm_label_list,
            ...    operation=lambda dt, i: need.orm
            ...        .find()
            ...        .where(label_id=dt[i].id)
            ...        .limit((page - 1) * PAGE_SIZE, PAGE_SIZE)
            ...        .end()
            ...)
            >>> need_list = sm_label.datas
            >>> return Result.success(data=need_list.to_dict())


        :param cls:目标外键的类，注意不是对象，是类
        :param key_name:外键的id
        :param field_name:保存进去的字段名字，默认以表名命名
        :param data:使用已有的数据作为外键
        :param operation:自定义操作
        """
        child_obj = cls()
        if field_name is None:
            name = child_obj.get_tb_name()
        else:
            name = field_name
        self.datas = self.result if data is None else data
        for i in range(len(self.datas)):
            if not operation:
                data = child_obj.orm.filter(**{key_name: self.datas[i].id})
            else:
                data = operation(self.datas, i)
            self.datas[i].add_field(name, data.to_dict())
