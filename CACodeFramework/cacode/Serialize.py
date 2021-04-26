import copy

from CACodeFramework.util import JsonUtil


def list_of_groups(init_list, size):
    """
    将数据集按照一定数量分组并返回新数组
    """
    lo_groups = zip(*(iter(init_list),) * size)
    end_list = [list(i) for i in lo_groups]
    count = len(init_list) % size
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


class QuerySet(list):
    """
    执行database operation返回的结果集对象

    元类:
        list

    附加方法:
        first():
            返回结果集对象的第一个数据

        last():
            返回结果集对象的最后一位参数

        page(size):
            按照每一页有size数量的结果分页

        to_json():
            将结果集对象转json字符串


    Attr

    """

    def __init__(self, instance, base_data: list):
        """
        初始化传入结果集并附加上base_data数据集

        instance:
            序列化的实例对象

        base_data:
            初始化数据源
        """
        list.__init__([])
        self.__instance__ = instance
        for i in base_data:
            self.append(i)

    def first(self):
        """
        取得结果集的第一位参数
        """
        return self[0]

    def last(self):
        """
        取得结果集的最后一位参数
        """
        return self[len(self) - 1]

    def page(self, size):
        """
        将结果集按照指定数目分割
        """
        return list_of_groups(self, size)

    def to_json(self, bf=False):
        """
        将结果集对象转json处理
        :param bf:是否需要美化sql
        """
        this_dict = JsonUtil.parse(obj=self, end_load=True)
        result = []
        # 取得隐藏参数
        show_fields = self.__instance__.__fields__
        # 过滤不需要序列化的参数
        for i, v in enumerate(this_dict):
            children = {}
            for sf in show_fields:
                if sf in v.keys():
                    children[sf] = this_dict[i][sf]

            result.append(children)

        return JsonUtil.parse(obj=result, bf=bf)

    def add_field(self, key):
        self.__instance__.__fields__.append(key)
