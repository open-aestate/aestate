import ctypes

dll_h = ctypes.windll.kernel32
LANG = hex(dll_h.GetSystemDefaultUILanguage())


class i18n:
    """

    """
    langs = {
        # 中文(简体,中国)
        0x804: {},
        # 中文（繁体，中国台湾）
        0x404: {},
        # 中文（繁体，香港特别行政区）
        0x413: {},
        # 英语
        0x409: {},
        # 法语
        0x40C: {},
        # 日语
        0x411: {},
    }

    @staticmethod
    def t(name):
        global LANG
        if LANG not in i18n.langs.keys():
            LANG = 0x804
            raise Exception(i18n.t('not_i18n'))
        if name not in i18n.langs.get(LANG).keys():
            return name
        return i18n.langs.get(LANG).get(name)
