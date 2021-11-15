from aestate.ajson import aj

from aestate.exception import FieldNotExist
from aestate.util.Log import ALog
from aestate.dbs import _mysql
from aestate.dbs import _mssql
from aestate.work.Adapter import LanguageAdapter

DB_KWARGS = {
    'pymysql': _mysql,
    'pymssql': _mssql
}


class MySqlConfig(_mysql.ParseUtil):
    """
    配置类:
        默认必须携带操作数据库所需的参数:
            - host:数据库地址
            - port:端口
            - database:数据库名
            - user:用户名
            - password:密码
            - charset:编码默认utf8
            - conf:其他配置
    """

    def __init__(self, db_type, *args, **kwargs):
        """
        可用于mysql的示例参数
        :param host:数据库地址
        :param port:端口
        :param database:数据库名
        :param user:用户名
        :param password:密码
        :param charset:编码默认utf8
        :param creator:创建者
        """

        if db_type is None:
            ALog.log_error(msg="The creator is missing, do you want to set`db_type='pymysql'`?",
                           obj=FieldNotExist, raise_exception=True)
        self.creator = __import__(db_type)
        self.opera = DB_KWARGS[db_type].OperaBase
        self.sqlFields = DB_KWARGS[db_type].Fields()
        self.kw = kwargs
        # 适配器
        if 'adapter' not in kwargs.keys():
            self.adapter = LanguageAdapter()
        super(MySqlConfig, self).__init__()

    def get(self):
        """
        获取当前配置类
        :return:
        """
        return self

    def set_field(self, key, value):
        """
        设置字段
        :param key:键
        :param value:值
        :return:
        """
        setattr(self, key, value)

    def get_field(self, name):
        """
        获取字段
        :param name:
        :return:
        """
        if hasattr(self, name):
            return getattr(self, name)
        return None

    def get_dict(self):
        """
        将配置类转转字典
        :return:
        """
        return self.__dict__

    def get_json(self, bf=False):
        """
        将配置类转json
        :return:
        """
        return aj.parse(self.get_dict(), bf)
