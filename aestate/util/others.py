# 社会因懒人而得到进步
import ajson


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


class CaseItem:
    def __init__(self, flag, method, *args, **kwargs):
        self.flag = flag
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return str(self.flag)


class CaseOperaBase:
    def __init__(self, val, method=None, *args, **kwargs):
        self.val = val
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def item(self, val, order) -> object: ...


class Case(CaseOperaBase):

    def __gt__(self, other):
        """
        左边大于右边
        """

        return self

    def __ge__(self, other):
        return int(self.val) <= int(other)

    def __lt__(self, other):
        """
        左边小于右边
        """
        return int(self.val) < int(other)

    def __le__(self, other):
        """
        左边小于等于右边
        """
        return int(self.val) >= int(other)

    def __eq__(self, other):
        """
        等于
        """
        return self.val == other

    def __ne__(self, other):
        """
        不等于
        """
        return self.val != other

    def item(self, val, order):
        order.opera[self.val] = CaseItem(self.val == val, self.method, self.args[0], **self.kwargs)
        return order


class CaseDefault(CaseOperaBase):
    def item(self, val, order):
        # order.opera[self.val] = CaseItem(True, val, *self.args, **self.kwargs)
        return order.end(self.val)


class Switch:
    """
    弥补python没有switch的缺陷
    使用教程：
            from aestate.util.others import Switch,Case,CaseDefault

            base_symbol = lambda x: x + x

            val = 3
        方式1：
            # case(选择性参数,满足条件时执行的方法,当满足条件后中间方法需要的参数)
            source = Switch(Case(val)) + \
                     Case(0, base_symbol, val) + \
                     Case(1, base_symbol, val) + \
                     Case(2, base_symbol, val) + \
                     Case(3, base_symbol, val) + \
                     Case(4, base_symbol, val) + \
                     Case(5, base_symbol, val) + \
                     CaseDefault(lambda: False)
            print(ajson.aj.parse(source, bf=True))
        方式2：
            source = Switch(Case(val)). \
            case(0, base_symbol, val). \
            case(1, base_symbol, val). \
            case(2, base_symbol, val). \
            case(3, base_symbol, val). \
            case(4, base_symbol, val). \
            case(5, base_symbol, val). \
            end(lambda: False)
        print(ajson.aj.parse(source, bf=True))
    """

    def __init__(self, val):
        self.val = val
        self.opera = {}

    def case(self, item, method, *args, **kwargs):
        if item in self.opera.keys():
            raise KeyError(f'`{item}` 已存在于case中')

        self.opera[item] = CaseItem(self.val == item, method, *args, **kwargs)
        return self

    def end(self, default_method, *args, **kwargs):
        """
        默认处理函数
        """

        for k, v in self.opera.items():
            if v.flag:
                return v.method(*v.args, **v.kwargs)
        return default_method(*args, **kwargs)

    def __add__(self, other):
        return other.item(self.val, self)


def test_switch():
    base_symbol = lambda x: x + x
    val = 3

    source = Switch(Case(val)) + \
             Case(0, base_symbol, val) + \
             Case(1, base_symbol, val) + \
             Case(2, base_symbol, val) + \
             Case(3, base_symbol, val) + \
             Case(4, base_symbol, val) + \
             Case(5, base_symbol, val) + \
             CaseDefault(lambda: False)
    print(ajson.aj.parse(source, bf=True))

    source = Switch(Case(val)). \
        case(0, base_symbol, val). \
        case(1, base_symbol, val). \
        case(2, base_symbol, val). \
        case(3, base_symbol, val). \
        case(4, base_symbol, val). \
        case(5, base_symbol, val). \
        end(lambda: False)
    print(ajson.aj.parse(source, bf=True))


def test_d():
    dict_data = {
        'a': 1,
        'b': {
            'a': [1]
        },
        'c': [
            {
                'a': 1,
                'b': {
                    'a': {
                        'a': [{
                            'a': [1]
                        }, {
                            'a': [1]
                        }]
                    }
                },
            }
        ]
    }
    d = DictToObject.conversion(dict_data)
    print(ajson.aj.parse(d, True))


if __name__ == '__main__':
    test_d()
