# 社会因懒人而得到进步
class DictTemplate(object):
    """
    字典对象模板
    """

    def __init__(self, init_data):
        self.init_data = init_data

    def add(self, key, obj):
        setattr(self, key, obj)


class DictToObject(object):
    """
    将字典转成对象，解决懒得写中括号
    """

    def __init__(self, dict_data):
        baseClass = DictTemplate(dict_data)
        self.dict_data = dict_data
        self.baseNode = baseClass
        self.verification(self.baseNode, self.dict_data)

    @staticmethod
    def conversion(dict_data: dict):
        node = DictToObject(dict_data)
        return node.baseNode

    def verification(self, node: DictTemplate, value):
        """
        验证模块
        """
        node.init_data = value
        if isinstance(value, dict):
            for key, val in value.items():
                if isinstance(val, (dict, list, tuple)):
                    val = self.verification(DictTemplate(val), val)
                node.add(key, val)

        elif isinstance(value, list):
            list_temp = []
            for val in value:
                if isinstance(val, (dict, list, tuple)):
                    val = self.verification(DictTemplate(val), val)
                list_temp.append(val)
            node.add('', list_temp)

        return node


if __name__ == '__main__':
    dict_data = {
        'a': 1,
        'b': {
            'a': [1]
        },
        'c': [
            {
                'a': 1
            }
        ]
    }
    d = DictToObject.conversion(dict_data)
    print(d.c)
