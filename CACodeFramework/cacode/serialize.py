import copy

from CACodeFramework.util import JsonUtil


def list_of_groups(init_list, size):
    lo_groups = zip(*(iter(init_list),) * size)
    end_list = [list(i) for i in lo_groups]
    count = len(init_list) % size
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


class QuerySet(list):

    def __init__(self, instance, base_data: list):
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

    def to_json(self):
        this_dict = JsonUtil.parse(obj=self, end_load=True)
        result = []
        show_fields = self.__instance__.__fields__
        for i, v in enumerate(this_dict):
            children = {}
            for sf in show_fields:
                if sf in v.keys():
                    children[sf] = this_dict[i][sf]

            result.append(children)

        return JsonUtil.parse(obj=result)

    def __str__(self):
        return JsonUtil.parse(self)
