import datetime
import os
import sys
import threading
from aestate.cacode.Modes import Singleton
from aestate.exception import e_fields
from aestate.util import others


class FieldsLength:
    DATETIME_FORMAT = 27
    INFO_FORMAT = 10
    LINE_FORMAT = 13
    OPERATION_FORMAT = 32
    HEX_FORMAT = 17
    CLASS_FORMAT = 70
    TASK_FORMAT = 15


class ConsoleColor:
    """
    控制台类型
    """

    class FontColor:
        # 黑色
        BLACK = 30
        # 红色
        RED = 31
        # 绿色
        GREEN = 32
        # 黄色
        YELLOW = 33
        # 蓝色
        BLUE = 34
        # 紫红色
        FUCHSIA = 35
        # 青蓝色
        CYAN = 36
        # 白色
        WHITE = 37
        # 成功的颜色 和 info的颜色
        SUCCESS_COLOR = GREEN
        # 失败的颜色 和 错误的颜色
        ERROR_COLOR = FUCHSIA
        # 警告的颜色
        WARNING_COLOR = YELLOW

    class BackgroundColor:
        # 黑色
        BLACK = 40
        # 红色
        RED = 41
        # 绿色
        GREEN = 42
        # 黄色
        YELLOW = 43
        # 蓝色
        BLUE = 44
        # 紫红色
        FUCHSIA = 45
        # 青蓝色
        CYAN = 46
        # 白色
        WHITE = 47

    class ShowType:
        # 默认
        DEFAULT = 0
        # 高亮
        HIGHLIGHT = 1
        # 下划线
        UNDERSCORE = 4
        # 闪烁
        FLASHING = 5
        # 反显
        REVERSE = 7
        # 不可见
        INVISIBLE = 8


class ConsoleWrite:
    def __init__(self):
        self.fontColor = ConsoleColor.FontColor.GREEN
        self.showType = ConsoleColor.ShowType.DEFAULT
        self.backColor = None

    @staticmethod
    def write(messages, consoleWriteObj):
        prefix = "{};".format(consoleWriteObj.showType) if consoleWriteObj.showType is not None else ""
        center = ";".format(consoleWriteObj.backColor) if consoleWriteObj.backColor is not None else ""
        suffix = "{}m{}".format(consoleWriteObj.fontColor, messages)
        out = "\033[{}{}{}\033[0m".format(prefix, center, suffix)
        print(out)


def write(path, content, max_size):
    """
    写出文件
    :param path:位置
    :param content:内容
    :param max_size:文件保存的最大限制
    :return:
    """
    _sep_path = path.split(os.sep)
    _path = ''
    for i in _sep_path:
        _end = _sep_path[len(_sep_path) - 1]
        if i != _end:
            _path += str(i) + os.sep
        else:
            _path += str(i)
        if not os.path.exists(_path):
            if '.' not in i:
                os.makedirs(_path)

    with open(os.path.join(_path), mode="a", encoding="UTF-8") as f:
        f.write(content)
        f.close()
    _size = os.path.getsize(_path)
    if _size >= max_size:
        os.remove(_path)
        # 递归
        write(path, content, max_size)


class CACodeLog(object):
    _instance_lock = threading.RLock()

    def __init__(self, path, print_flag=False, save_flag=False, max_clear=10):
        """

        初始化配置

        :param path:保存的路径

        :param print_flag:是否打印日志 默认False

        :param save_flag:是否保存日志 默认False

        :param max_clear:日志储存最大限制,默认10MB 单位:MB

        """
        self.max_clear = max_clear * 1024 * 1000
        self.path = path
        self.print_flag = print_flag
        self.save_flag = save_flag

    @staticmethod
    def pure_log(msg, consoleWriteObj=ConsoleWrite):
        """
        输出任务执行日志

        :param obj:执行日志的对象地址
        :param msg:消息
        :param line:被调用前的行数
        :param task_name:任务对象的值
        :param LogObject:写出文件的对象

        """
        ConsoleWrite.write(messages=msg, consoleWriteObj=consoleWriteObj())

    @staticmethod
    def log(msg, obj=None, line=sys._getframe().f_back.f_lineno,
            task_name='Task', LogObject=None, field=e_fields.Info(), func=None,
            consoleWriteObj=ConsoleWrite()):
        """
        输出任务执行日志

        :param obj:执行日志的对象地址
        :param msg:消息
        :param line:被调用前的行数
        :param task_name:任务对象的值
        :param LogObject:写出文件的对象

        """

        def fullname(o):

            module = o.__class__.__module__
            if module is None or module == str.__class__.__module__:
                return o.__class__.__name__  # Avoid reporting __builtin__
            else:
                return module + '.' + o.__class__.__name__

        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        try:
            if obj is not None:
                write_repr = fullname(obj)
            else:
                write_repr = 'OBJECT IS NULL'
        except TypeError as err:
            write_repr = 'OBJECT CAN`T NOT PARSE'
        # write_repr = repr if repr and not repr_c else repr_c[0] if repr_c else type(obj)
        # 格式：时间 类型 日志名称 对象地址 被调用行号 执行类型 信息
        t = f"[{t}]".ljust(FieldsLength.DATETIME_FORMAT)
        field = f"[{field}]".ljust(FieldsLength.INFO_FORMAT)
        line = f"[line:{line}]".ljust(FieldsLength.LINE_FORMAT)
        hex_id = f"[{hex(id(obj))}]".ljust(FieldsLength.HEX_FORMAT)
        write_repr = f"[{write_repr}]".ljust(FieldsLength.CLASS_FORMAT)
        task_name = f"[{task_name}]".ljust(FieldsLength.TASK_FORMAT)
        msg = f":{msg}"

        info = "{}{}{}{}{}{}{}".format(t, field, line, hex_id, write_repr, task_name, msg)
        ConsoleWrite.write(messages=info, consoleWriteObj=consoleWriteObj)
        # 输出日志信息
        # file = sys.stdout
        # file.write(info)
        # print(f"\033[4;31m{info}\033[0m")
        # warnings.warn_explicit(info, category=Warning, filename='line', lineno=line)
        if LogObject is not None:
            if func is None:
                func = LogObject.warn
            func(info)

        return info

    @staticmethod
    def warning(msg, obj=None, line=sys._getframe().f_back.f_lineno, task_name='Task', LogObject=None):

        consoleWrite = ConsoleWrite()
        consoleWrite.fontColor = ConsoleColor.FontColor.WARNING_COLOR

        CACodeLog.log(msg=msg, obj=obj, line=line, task_name=task_name, LogObject=LogObject, field=e_fields.Warn(),
                      func=LogObject.warn if LogObject is not None else None,
                      consoleWriteObj=consoleWrite)

    @staticmethod
    def log_error(msg, obj=None, line=sys._getframe().f_back.f_lineno, task_name='Task', LogObject=None,
                  raise_exception=False):
        """
        :param msg:描述
        :param line:行
        :param obj:执行的对象，当允许抛出异常时，则指明该对象为一个Exception或他的子类
        :param task_name:线程唯一名称
        :param LogObject:日志对象
        :param raise_exception:是否抛出异常
        """
        if raise_exception:
            raise obj(msg)

        consoleWrite = ConsoleWrite()
        consoleWrite.fontColor = ConsoleColor.FontColor.ERROR_COLOR

        CACodeLog.log(msg=msg, obj=obj, line=line, task_name=task_name, LogObject=LogObject, field=e_fields.Error(),
                      func=LogObject.warn if LogObject is not None else None,
                      consoleWriteObj=consoleWrite)

    @staticmethod
    def err(cls, msg, LogObject=None):
        if LogObject is not None:
            LogObject.error(msg)
        raise cls(msg)

    def success(self, content):
        """
        成功日志
        :param content:内容
        :return:
        """
        _path = "%s%s%s%s" % (os.sep, 'success', os.sep, 'log.log')
        self.log_util(_path, content)

    def error(self, content):
        """
        错误日志
        :param content:内容
        :return:
        """
        _path = "%s%s%s%s" % (os.sep, 'error', os.sep, 'log.log')
        self.log_util(_path, content)

    def warn(self, content):
        """
        警告日志
        :param content:内容
        :return:
        """
        _path = "%s%s%s%s" % (os.sep, 'warn', os.sep, 'log.log')
        self.log_util(_path, content)

    def log_util(self, path_str, content):
        """
        日志工具,勿用
        :param path_str:
        :param content:
        :return:
        """
        path = self.get_path(path_str)
        _date = others.date_format()
        # _log = '[%s]\t[%s] - %s\r\n' % (_date, 'content', str(content))
        if self.print_flag:
            self.log(content)
        if self.save_flag:
            write(path, content, self.max_clear)

    def get_path(self, end_path):
        """
        日志类获取绝对路径
        :param end_path:
        :return:
        """
        _STATIC_TXT = os.path.join('', self.path + end_path)
        return _STATIC_TXT

    def __new__(cls, *args, **kwargs):

        # if Db_opera.instance is None:
        #     Db_opera.instance = object.__new__(cls)
        # return Db_opera.instance
        instance = Singleton.createDbOpera(cls)
        return instance
