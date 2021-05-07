import copy

from CACodeFramework.cacode.Serialize import QuerySet
from CACodeFramework.exception import e_fields
from CACodeFramework.field import MySqlDefault
from CACodeFramework.opera import op_db
from CACodeFramework.util.Log import CACodeLog

from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.util import DbUtil

# 每个任务唯一ID
import uuid


# from CACodeFramework.util.ParseUtil import ParseUtil


class Repository:
    """
    - POJO类
        - 继承该类表名此类为数据库的pojo类
        - 需要配合:@Table(name, msg, **kwargs)使用
    """

    def __init__(self, config_obj=None, instance=None, log_conf=None, close_log=False, serializer=QuerySet, **kwargs):
        """作者:CACode 最后编辑于2021/4/30

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

            使用本类需要携带一个来自CACodeFramework.util.Config.config的配置类,详见:CACodeFramework.util.Config.config

        Attributes:
            以下的字段均可覆盖重写

            config_obj:数据源配置类

            log_conf:日志配置工具

            log_obj:日志对象

            close_log:是否关闭日志

            serializer:序列化使用的类,默认使用CACodeFramework.cacode.Serialize.QuerySet

            instance:实例

            __table_name__:表名称

            operation:操作类的实现

            fields:操作的字段

            sqlFields:sql方言

        :param config_obj:配置类
        :param log_conf:日志配置类
        :param close_log:是否关闭日志显示功能
        :param serializer:自定义序列化器,默认使用CACodeFramework.cacode.Serialize.QuerySet
        """
        # 以下使用ParseUtil将所有参数替换为可动态修改
        # 有没有关闭日志
        # 数据源配置
        self.ParseUtil = config_obj
        ParseUtil = self.ParseUtil
        ParseUtil.set_field_compulsory(self, key='config_obj', data=kwargs, val=config_obj)
        ParseUtil.set_field_compulsory(obj=self, data=kwargs, key='abs', val=False)
        # 当本类为抽象类时，仅设置所需要的值
        ParseUtil.set_field_compulsory(self, key='close_log', data=kwargs, val=close_log)
        if hasattr(self, 'close_log') and not self.close_log and not self.abs:
            CACodeLog.warning(obj=self, msg='Being Initialize this object')
        # 有没有表名
        ParseUtil.set_field_compulsory(self, key='__table_name__', data=kwargs,
                                       val=self.__table_name__ if hasattr(self, '__table_name__') else
                                       "`__table_name__` parsing failed")
        # 参照对象
        ParseUtil.set_field_compulsory(self, key='instance', data=kwargs, val=instance)
        # 取得字段的名称
        ParseUtil.set_field_compulsory(self, key='fields', data=kwargs, val=list(instance.getFields().keys()))
        # 当当前类为抽象类时，为类取消初始化数据库配置
        if not self.abs:
            # 操作类
            ParseUtil.set_field_compulsory(self, key='operation', data=kwargs, val=op_db.DbOperation())
            # 获取sql方言配置
            ParseUtil.set_field_compulsory(self, key='sqlFields', data=kwargs, val=MySqlDefault.MySqlFields_Default())
            # 连接池
            if hasattr(self, 'config_obj') and self.config_obj:
                self.db_util = DbUtil.Db_opera(host=ParseUtil.fieldExist(self.config_obj, 'host'),
                                               port=ParseUtil.fieldExist(self.config_obj, 'port'),
                                               user=ParseUtil.fieldExist(self.config_obj, 'user'),
                                               password=ParseUtil.fieldExist(self.config_obj, 'password'),
                                               database=ParseUtil.fieldExist(self.config_obj, 'database'),
                                               charset=ParseUtil.fieldExist(self.config_obj, 'charset'),
                                               creator=ParseUtil.fieldExist(self.config_obj, 'creator',
                                                                            raise_exception=True),
                                               POOL=None if 'POOL' not in kwargs.keys() else kwargs['POOL'])
            else:
                CACodeLog.err(AttributeError, e_fields.Miss_Attr('`config_obj` is missing'))

            ParseUtil.set_field_compulsory(self, key='result', data=kwargs, val=None)
            ParseUtil.set_field_compulsory(self, key='log_obj', data=kwargs,
                                           val=CACodeLog(**log_conf) if log_conf is not None else None)
            ParseUtil.set_field_compulsory(self, key='serializer', data=kwargs, val=serializer)
        # 移除name和msg键之后,剩下的就是对应的数据库字段
        # 设置表名
        # 是否关闭打印日志
        # self.__table_name__ = self.__table_name__
        # self.operation = op_db.DbOperation()
        # 模板类
        # self.instance = instance
        # 该对象的所有字段
        # fds = instance.fields
        # self.fields = list(fds.keys())
        # 配置类
        # self.config_obj = config_obj
        # 操作数据库
        # self.db_util = DbUtil.Db_opera(host=self.config_obj.host,
        #                                port=self.config_obj.port,
        #                                user=self.config_obj.user,
        #                                password=self.config_obj.password,
        #                                database=self.config_obj.database,
        #                                charset=self.config_obj.charset)
        # 配置日志
        # self.log_obj = None
        # if log_conf is not None:
        #     self.log_obj = LogObj(**log_conf)
        # 返回的结果
        # self.result = None
        # 序列化器
        # self.serializer = serializer

    def conversion(self):
        """作者:CACode 最后编辑于2021/4/12

        将此Repository转换为ORM实体

        Return:
            ORM转换之后的实体对象
        """
        return CACodePureORM(self, serializer=self.serializer)

    def first(self):
        """
        获取数据库中的第一个
        """
        self.conversion().top().end()

    def last(self):
        """
        获取最后一个参数
        """

    def find_all(self):
        """作者:CACode 最后编辑于2021/4/12

        从当前数据表格中查找所有数据

        Returns:
            将所有结果封装成POJO对象集合并返回数据
        """
        # 设置名称
        name = str(uuid.uuid1())
        # 开启任务
        kwargs = {
            'func': self.operation.__find_all__,
            '__task_uuid__': name,
            't_local': self
        }
        result = self.operation.start(*self.fields, **kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)

        return self.result

    def find_field(self, *args):
        """作者:CACode 最后编辑于2021/4/12

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
        kwargs = {'func': self.operation.__find_by_field__, '__task_uuid__': name, 't_local': self}

        result = self.operation.start(*args, **kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def find_one(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

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
        self.result = self.find_many(**kwargs)
        if self.result is None or len(self.result) == 0:
            return None
        else:
            return self.result[0]

    def find_many(self, **kwargs):
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
        # 开启任务
        kwargs['func'] = self.operation.__find_many__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        result = self.operation.start(**kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def find_sql(self, **kwargs):
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
        # 开启任务
        kwargs['func'] = self.operation.__find_sql__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        result = self.operation.start(**kwargs)

        self.result = self.serializer(instance=self.instance, base_data=result)
        return self.result

    def update(self, **kwargs):
        """
        执行更新操作:
            返回受影响行数
        pass:
            删除也是更新操做
        :param kwargs:包含所有参数:
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :return:
        """
        kwargs['config_obj'] = self.config_obj
        kwargs = self.ParseUtil.print_sql(**kwargs)
        kwargs = self.ParseUtil.last_id(**kwargs)
        return self.db_util.update(**kwargs)

    def insert_sql(self, **kwargs):
        """
        使用sql插入
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :return rowcount,last_id if last_id=True
        """
        kwargs = self.ParseUtil.print_sql(**kwargs)
        kwargs = self.ParseUtil.last_id(**kwargs)
        return self.db_util.insert(**kwargs)

    def save(self, **kwargs):
        """
        将当前储存的值存入数据库
        """
        kwargs['pojo'] = self
        return self.create(**kwargs)

    def create(self, **kwargs):
        """
        插入属性:
            返回受影响行数
        :param kwargs:包含所有参数:
            pojo:参照对象
            last_id:是否需要返回最后一行数据,默认False
        :return:rowcount,last_id if last_id=True
        """
        # 设置名称
        name = str(uuid.uuid1())
        # 开启任务
        kwargs['func'] = self.operation.__insert__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        self.result = self.operation.start(**kwargs)
        return self.result

    def copy(self):
        """
        复制对象进行操做
        """
        return copy.copy(self)
