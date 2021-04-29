class FieldControl:
    """
    将sql方言转可控制与配置

    利用动态语言特性
    """

    def __init__(self):
        self.fields = []

    def setField(self, name, value):
        """
        设置一个sql方言

        名字格式:
            select_str:以关键字开头,_str结尾
            order_by_str:多个字段以下划线分割,_str结尾

        """
        pass

    def getFunction(self, name):
        pass

    def formatFromDict(self, data: dict):
        """
        从字典中读取方言
        """
        for k, v in data.items():
            self.fields.append({
                str(k)[0:len(k) - 1].replace('_', ' '), v
            })

    def formatFromFile(self, path):
        with open(path, 'r') as f:
            json_text = ''
            line = f.readline()
            while line:
                json_text += line
            f.close()
