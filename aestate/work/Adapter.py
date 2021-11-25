from aestate.exception import FieldNotExist
from aestate.util.Log import ALog


class LanguageAdapter:
    """
    适配器,将sql方言适配到ORM框架中,实现sql自由

    从配置表中开始配置sql方言,继承SqlLanguage类并实现抽象方法,开启

    实现当前类，在orm操作中存在自定义字段时，保证所有的操作都能够按照你所希望的那样执行
    """
    funcs = {}

    def __init__(self):
        if not hasattr(self, 'funcs'):
            self.funcs = {}
        self.__sp('like', self._like_opera)
        self.__sp('in', self._in_opera)
        self.__sp('lt', self._lt_opera)
        self.__sp('gt', self._gt_opera)
        self.__sp('le', self._le_opera)
        self.__sp('ge', self._ge_opera)
        self.__sp('eq', self._eq_opera)

    def add_lan(self, name, func):
        self.__sp(name, func)

    def _like_opera(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' LIKE ')
        instance.args.append('%s')
        instance.args.append(' AND ')
        instance.params.append(value)

    def _in_opera(self, instance, key, value):
        if isinstance(value, list):
            instance.args.append('`' + key + '`')
            instance.args.append(' IN ')
            value = [str(i) for i in value]
            vals = ','.join(value)
            instance.args.append(f'( {vals} )')
        else:
            ALog.log_error(
                msg='value type is not list or QuerySet object',
                obj=FieldNotExist, raise_exception=True)

    def _lt_opera(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' < ')
        instance.args.append('%s')
        instance.args.append(' AND ')
        instance.params.append(value)

    def _gt_opera(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' > ')
        instance.args.append('%s')
        instance.args.append(' AND ')
        instance.params.append(value)

    def _le_opera(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' <= ')
        instance.args.append('%s')
        instance.params.append(value)

    def _ge_opera(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' >= ')
        instance.args.append('%s')
        instance.params.append(value)

    def _eq_opera(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' = ')
        instance.args.append('%s')
        instance.params.append(value)

    def __sp(self, key, val):
        if key not in self.funcs.keys():
            self.funcs[key] = val
