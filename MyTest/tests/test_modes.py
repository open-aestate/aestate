# 社会因懒人而得到进步
import ajson

from aestate.cacode.Modes import Switch, Case, CaseDefault, DictToObject


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
