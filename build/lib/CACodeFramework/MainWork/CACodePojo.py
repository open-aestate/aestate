from CACodeFramework.util import JsonUtil


class POJO(object):

    def to_json(self):
        """
        将此对象转换为json
        无视时间报错
        """
        return JsonUtil.parse(self.__dict__)

    def to_dict(self):
        """
        将此对象转换成字典格式
        """
        return self.__dict__
