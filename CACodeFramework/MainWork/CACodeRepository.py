import copy

from CACodeFramework.cacode.Serialize import QuerySet
from CACodeFramework.opera import op_db
from CACodeFramework.util.Log import CACodeLog

from CACodeFramework.MainWork.CACodePureORM import CACodePureORM
from CACodeFramework.util import DbUtil
import threading

# 每个任务唯一ID
import uuid

# threadLocal 避免线程干扰
from CACodeFramework.util.ParseUtil import ParseUtil

t_local = threading.local()


# 线程锁


class LogObj(CACodeLog):
    """
    继承CACodeLog，配置
    """

    def __init__(self, **kwargs):
        """
        继承原始父类
        """
        super(LogObj, self).__init__(**kwargs)


class Repository(object):
    """
    - POJO类
        - 继承该类表名此类为数据库的pojo类
        - 需要配合:@Table(name, msg, **kwargs)使用
    """

    def __init__(self, config_obj=None, participants=None, log_conf=None, close_log=False, serialize=QuerySet):
        """作者:CACode 最后编辑于2021/4/27

        通过继承此类将数据表实体化

            实体化之后你可以使用像类似find_one()等操做

            可以调用conversion()方法将其转化为ORM框架常用的样式

            无需担心类型问题，无需担心datetime无法转换
        使用方法:
            #加入Table注解，并标注表名与描述，因考虑后期优化问题，请务必填写MSG参数

            @Table(name="demo_table", msg="demo message")

            #继承Repository并得到相对应的半自动ORM操做
            class TestClass(Repository):
                # 初始化并super配置
                def __init__(self):
                    super(TestClass, self).__init__(config_obj=ConF(), participants=Demo())

        初始化配置:

            使用本类需要携带一个来自CACodeFramework.util.Config.config的配置类,详见:CACodeFramework.util.Config.config

        :param config_obj:配置类
        :param log_conf:日志配置类
        :param close_log:是否关闭日志显示功能
        :param serialize:自定义序列化器,默认使用CACodeFramework.cacode.Serialize.QuerySet
        """
        # 移除name和msg键之后,剩下的就是对应的数据库字段
        # 设置表名
        # 是否关闭打印日志
        self.close_log = close_log
        self.__table_name__ = self.__table_name__
        self.operation = op_db.DbOperation()
        if not self.close_log:
            CACodeLog.log(obj=self, msg='Being Initialize this object')
        # 模板类
        self.participants = participants
        # 该对象的所有字段
        fds = participants.fields
        self.fields = list(fds.keys())
        # 配置类
        self.config_obj = config_obj
        # 操作数据库
        self.db_util = DbUtil.Db_opera(host=self.config_obj.host,
                                       port=self.config_obj.port,
                                       user=self.config_obj.user,
                                       password=self.config_obj.password,
                                       database=self.config_obj.database,
                                       charset=self.config_obj.charset)
        # 设定返回值
        self._result = None

        # 配置日志
        self.log_obj = None
        if log_conf is not None:
            self.log_obj = LogObj(**log_conf)
        # 返回的结果
        self.result = None
        # 序列化器
        self.serialize = serialize

    def conversion(self):
        """作者:CACode 最后编辑于2021/4/12

        将此Repository转换为ORM实体

        Return:
            ORM转换之后的实体对象
        """
        return CACodePureORM(self)

    def find_all(self):
        """作者:CACode 最后编辑于2021/4/12

        从当前数据表格中查找所有数据

        Returns:
            将所有结果封装成POJO对象集合并返回数据
        """
        # 设置名称
        name = str(uuid.uuid1())
        # 开启任务
        kwargs = {'func': self.operation.__find_all__, '__task_uuid__': name, 't_local': self}
        self.result = self.operation.start(*self.fields, **kwargs)
        return self.result

    def find_by_field(self, *args):
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

        self.result = self.operation.start(*args, **kwargs)

        return self.result

    def find_one(self, **kwargs):
        """作者:CACode 最后编辑于2021/4/12

        查找第一条数据

            可以是一条

            也可以是很多条中的第一条

        code:

            _result = self.find_many(**kwargs)
            if len(_result) == 0:
                return None
            else:
                return _result[0]

        :param kwargs:包含所有参数:

            pojo:参照对象

            last_id:是否需要返回最后一行数据,默认False

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
        """作者:CACode 最后编辑于2021/4/12

        查询出多行数据

            第一个必须放置sql语句

        :param kwargs:包含所有参数:

            pojo:参照对象

            last_id:是否需要返回最后一行数据,默认False

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
        self.result = self.operation.start(**kwargs)
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

        self.result = self.serialize(instance=self.participants, base_data=result)
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
        kwargs['config_obj'] = t_local.config_obj
        kwargs = ParseUtil.print_sql(**kwargs)
        kwargs = ParseUtil.last_id(**kwargs)
        return t_local.db_util.update(**kwargs)

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
        kwargs = ParseUtil.print_sql(**kwargs)
        kwargs = ParseUtil.last_id(**kwargs)
        return self.db_util.insert(**kwargs)

    def save(self, **kwargs):
        """
        将当前储存的值存入数据库
        """
        kwargs['pojo'] = self
        return self.insert_one(**kwargs)

    def insert_one(self, **kwargs):
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
        kwargs['func'] = self.operation.__insert_one__
        kwargs['__task_uuid__'] = name
        kwargs['t_local'] = self
        self.result = self.operation.start(**kwargs)
        return self.result

    def insert_many(self, **kwargs):
        """
        插入多行
            这个是用insert_one插入多行
        :param kwargs:包含所有参数:
            pojo_list:参照对象列表
            last_id:是否需要返回最后一行数据,默认False
            sql:处理过并加上%s的sql语句
            params:需要填充的字段
        :return:list[rowcount,last_id if last_id=True]
        """
        kwargs['config_obj'] = self.config_obj
        kwargs = ParseUtil.print_sql(**kwargs)
        kwargs = ParseUtil.last_id(**kwargs)
        t_local._result = []
        for item in kwargs['pojo_list']:
            kwargs['pojo'] = item
            t_local._result.append(self.insert_one(**kwargs))
        return t_local._result

    # def get_this(self):
    #     """
    #     获取当前仓库
    #     """
    #     return self

    def copy(self):
        """
        复制对象进行操做
        """
        return copy.copy(self)
