class LanguageAdapter:
    """
    适配器,将sql方言适配到ORM框架中,实现sql自由

    从配置表中开始配置sql方言,继承SqlLanguage类并实现抽象方法,开启

    实现当前类，在orm操作中存在自定义字段时，保证所有的操作都能够按照你所希望的那样执行
    """

    def __init__(self):
        if hasattr(self, 'funcs'):
            self.funcs['like'] = self.like
        else:
            self.funcs = {
                'like': self.like
            }

    def like(self, instance, key, value):
        instance.args.append('`' + key + '`')
        instance.args.append(' LIKE ')
        instance.args.append('%s')
        instance.params.append(value)
