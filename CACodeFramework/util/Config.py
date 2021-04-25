from CACodeFramework.util import JsonUtil


class config(object):
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

    def __init__(self, host, port, database, user, password, charset='utf8', conf=None):
        """
        必须要有的参数
        :param host:数据库地址
        :param port:端口
        :param database:数据库名
        :param user:用户名
        :param password:密码
        :param charset:编码默认utf8
        :param conf:其他配置
        """
        if conf is None:
            conf = {}
        self.conf = conf
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

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
        return None

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

    def get_json(self):
        """
        将配置类转json
        :return:
        """
        return JsonUtil.parse(self.get_dict())
