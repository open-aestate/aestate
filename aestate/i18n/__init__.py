import ctypes
import threading

from aestate.work.Modes import Singleton

dll_h = ctypes.windll.kernel32
LANG = dll_h.GetSystemDefaultUILanguage()


class I18n:
    """
    国际化语言,在统一配置下的全局语言解决方案
    """

    def __init__(self, langs=None):
        if langs is None:
            langs = {}
        self.langs = {
            # 中文(简体,中国)
            0x804: {
                'if_tag_not_test': 'if 标记中的属性`test` 缺少必需的结构',
                'xml_syntax_error': 'xml语法错误,不相等的逻辑运算符数量,在:%s',
                'before_else_not_if': '在 else 标签前面找不到 if 标签',
                'not_field_name': '被调用的方法中不存在名为 `%s` 的参数',
                'not_from_node_name': '无法从节点中找到名为 `%s` 的模板',
                'not_result_map': "找不到 resultMap 模板",
                'not_type': '无法从节点中找到名为 `type` 的属性'
            },
            # 中文（繁体，中国台湾）
            0x404: {

            },
            # 中文（繁体，香港特别行政区）
            0x413: {

            },
            # 英语
            0x409: {
                'if_tag_not_test': 'The attribute`test` in the if tag is missing a required structure',
                'xml_syntax_error': 'xml syntax error, unequal number of logical operators, from:%s',
                'before_else_not_if': 'Cannot find the if tag in front of the else tag',
                'not_field_name': 'The parameter named `%s` does not exist in the called method',
                'not_from_node_name': 'The template named `%s` could not be found from the node',
                'not_result_map': "Can't find resultMap template",
                'not_type': 'The attribute named `type` could not be found from the node'
            },
            # 法语
            0x40C: {},
            # 日语
            0x411: {},
        }
        self.langs.update(langs)

    _instance_lock = threading.RLock()

    def t(self, name):
        global LANG
        if LANG not in self.langs.keys():
            LANG = 0x804
            raise Exception(f'i18n field is not exist:{name}')
        if name not in self.langs.get(LANG).keys():
            return name
        return self.langs.get(LANG).get(name)

    def __new__(cls, *args, **kwargs):
        """
        单例管理缓存内容
        """
        instance = Singleton.createObject(cls)
        return instance


i18n = I18n()
