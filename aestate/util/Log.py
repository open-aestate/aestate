import datetime
import os
import sys
import threading
import traceback

from aestate.util.others import write, logTupleToText
from aestate.work.Cache import LogCache
from aestate.work.Modes import Singleton
from aestate.exception import LogStatus
from aestate.util import others
from aestate.work.commad import __log_logo__


class FieldsLength:
    DATETIME_FORMAT = 27
    INFO_FORMAT = 5
    LINE_FORMAT = 5
    OPERATION_FORMAT = 14
    # HEX_FORMAT = 17
    TASK_FORMAT = 7
    # CLASS_FORMAT = 70
    MSG_FORMAT = 0


class ConsoleColor:
    """
    控制台类型
    """

    class FontColor:
        # 黑色
        BLACK = 30
        # 灰色
        GRAY = 90
        # 粉色
        PINK = 31
        # 红色
        RED = 35
        # 绿色
        GREEN = 32
        # 浅绿色
        LIGHT_GREEN = 91
        # 黄色
        YELLOW = 33
        # 浅黄色
        LIGHT_YELLOW = 92
        # 深黄色
        DARK_YELLOW = 93
        # 紫色
        PURPLE = 34
        # 浅紫色
        LIGHT_PURPLE = 96
        # 青蓝色
        CYAN = 36
        # 白色
        WHITE = 37
        # 成功的颜色 和 info的颜色
        SUCCESS_COLOR = GREEN
        # 失败的颜色 和 错误的颜色
        ERROR_COLOR = RED
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

    # @staticmethod
    # def write(messages, consoleWriteObj=None):
    #     prefix = "{};".format(consoleWriteObj.showType) if consoleWriteObj.showType is not None else ""
    #     center = ";".format(consoleWriteObj.backColor) if consoleWriteObj.backColor is not None else ""
    #     suffix = "{}m{}".format(consoleWriteObj.fontColor, messages)
    #     out = "\033[{}{}{}\033[0m".format(prefix, center, suffix)
    #     print(out)

    @staticmethod
    def format_color(text, color=None):
        if color is not None:
            prefix = "{};".format(ConsoleColor.ShowType.DEFAULT)
            suffix = "{}m{}".format(color, text)
            out = "\033[{};{}\033[0m".format(prefix, suffix)
            return out
        return text


class ALog(object):
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
    def pure_log(msg, **kwargs):
        """
        输出任务执行日志

        :param msg:消息

        """
        ALog.log(msg=msg, **kwargs)

    @staticmethod
    def format_text(field: LogStatus, line, obj, task_name, msg, ned_text=False,
                    text_color: ConsoleColor.FontColor = None):
        """
        将字符串格式化成好看的颜色
        """
        try:
            if obj is not None:
                write_repr = others.fullname(obj)
            else:
                write_repr = 'OBJECT IS NULL'
        except TypeError:
            write_repr = 'OBJECT CAN`T NOT PARSE'
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        pure_text = ' '.join([str(t), str(field.value), str(line), str(hex(id(obj))),
                              '[{}]'.format(task_name), str(write_repr), f" : {msg}"])
        t = ConsoleWrite.format_color(f"{t}".ljust(FieldsLength.DATETIME_FORMAT), ConsoleColor.FontColor.CYAN)
        _field = ConsoleWrite.format_color(f"{field.value}".rjust(FieldsLength.INFO_FORMAT),
                                           ConsoleColor.FontColor.GREEN
                                           if field == LogStatus.Info
                                           else ConsoleColor.FontColor.RED
                                           if field == LogStatus.Error
                                           else ConsoleColor.FontColor.YELLOW
                                           if field == LogStatus.Warn
                                           else ConsoleColor.FontColor.YELLOW)
        line = f"{line}".rjust(FieldsLength.LINE_FORMAT)
        hex_id = ConsoleWrite.format_color(f" {str(hex(id(obj)))}", ConsoleColor.FontColor.PINK)
        task_name = ConsoleWrite.format_color(f"{task_name}".rjust(FieldsLength.TASK_FORMAT),
                                              ConsoleColor.FontColor.PURPLE)
        write_repr = ConsoleWrite.format_color(write_repr,
                                               ConsoleColor.FontColor.LIGHT_GREEN
                                               if field != LogStatus.Error
                                               else ConsoleColor.FontColor.RED)
        msg = ConsoleWrite.format_color(f" : {msg}", text_color)
        info = "{}{}{}{}{}{}{}".format(t, _field, line, hex_id, ' [{}] '.format(task_name), write_repr, msg)
        if ned_text:
            return info, pure_text
        return info

    @staticmethod
    def log(msg, obj=None, line=sys._getframe().f_back.f_lineno, task_name='TEXT', LogObject=None,
            field: LogStatus = LogStatus.Info, func=None,
            text_color: ConsoleColor.FontColor = None, **kwargs):
        """
        输出任务执行日志

        :param msg:消息
        :param obj:执行日志的对象地址
        :param line:被调用前的行数
        :param task_name:任务对象的值
        :param LogObject:写出文件的对象
        :param field:日志模式
        :param func:日志执行后的自定义操作
        """

        try:
            if obj is not None:
                write_repr = others.fullname(obj)
            else:
                write_repr = 'OBJECT IS NULL'
        except TypeError:
            write_repr = 'OBJECT CAN`T NOT PARSE'

        # write_repr = repr if repr and not repr_c else repr_c[0] if repr_c else type(obj)
        # 格式：时间 类型 被调用时行数 对象地址 日志信息 执行类 信息
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        con_text = ' '.join([str(t), str(field.value), str(line), str(hex(id(obj))),
                             '[{}]'.format(task_name), str(write_repr), f" : {msg}"])
        info = ALog.format_text(field, line, obj, task_name, msg, text_color=text_color)

        # print(info)

        def __log_obj_write__(_object):
            if _object is not None:
                if field == LogStatus.Info:
                    _object.info(con_text, pure_text=info, line=line, obj=obj)
                elif field == LogStatus.Error:
                    _object.error(con_text, pure_text=info, line=line, obj=obj)
                elif field == LogStatus.Warn:
                    _object.warn(con_text, pure_text=info, line=line, obj=obj)
                else:
                    _object.info(con_text, pure_text=info, line=line, obj=obj)
            else:
                print(info)

        if obj is not None:
            if hasattr(obj, 'log_obj'):
                __log_obj_write__(obj.log_obj)
            else:
                __log_obj_write__(LogObject)
        else:
            __log_obj_write__(LogObject)
        if func is not None:
            func(con_text)

        return info

    @staticmethod
    def warning(**kwargs):
        ALog.log(task_name='WARNING', field=LogStatus.Warn, **kwargs)

    @staticmethod
    def log_error(msg=None, obj=None, line=sys._getframe().f_back.f_lineno, task_name='ERROR',
                  LogObject=None, raise_exception=False):
        """
        :param msg:描述
        :param line:行
        :param obj:执行的对象，当允许抛出异常时，则指明该对象为一个Exception或他的子类
        :param task_name:线程唯一名称
        :param LogObject:日志对象
        :param raise_exception:是否抛出异常
        """
        text = list(msg)

        def get_stack():
            text.append('\n')
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()
            extracted_list = traceback.extract_tb(exc_traceback_obj)
            for item in traceback.StackSummary.from_list(extracted_list).format():
                text.append(item)

        if raise_exception:
            if isinstance(obj, type):
                try:
                    raise obj(msg)
                except obj:
                    get_stack()
                    text.append(f'{obj.__name__} :{msg}')
            else:
                get_stack()
                text.append(f'{obj.__class__.__name__} :{msg}')
        ALog.log(msg=''.join(text), obj=obj, line=line, task_name=task_name,
                 LogObject=LogObject if LogObject is not None else None, field=LogStatus.Error,
                 text_color=ConsoleColor.FontColor.RED)

    def template(self, status: LogStatus, *content, **kwargs):
        """
        日志的模板,error、info和warn都在这里执行
        """
        # 从缓存中获取日志的对象
        log_cache = LogCache()
        # 从缓存中获取文件名,因为不能每次查询都生成一个文件,这样做是不合理的
        _path = log_cache.get_filename(self.path, self.max_clear, status)
        if status == LogStatus.Info:
            logo_show = 'info_logo_show'
        elif status == LogStatus.Warn:
            logo_show = 'warn_logo_show'
        elif status == LogStatus.Error:
            logo_show = 'error_logo_show'
        else:
            logo_show = 'info_logo_show'
        # 如果日志中没有打印过logo,就写入logo
        ls = getattr(log_cache, logo_show)
        if not ls:
            setattr(log_cache, logo_show, True)
            self.log_util(_path, __log_logo__)
        self.log_util(_path, *content)
        line = kwargs['line'] if 'line' in kwargs.keys() else sys._getframe().f_back.f_lineno
        obj = kwargs['obj'] if 'obj' in kwargs.keys() else self
        text = kwargs['pure_text'] \
            if 'pure_text' in kwargs.keys() \
            else ALog.format_text(status, line, obj, status.value, logTupleToText(False, *content))
        print(text)

    def info(self, *content, **kwargs):
        """
        成功日志
        :param content:内容
        :return:
        """
        self.template(LogStatus.Info, *content, **kwargs)

    def warn(self, *content, **kwargs):
        """
        警告日志
        :param content:内容
        :return:
        """
        self.template(LogStatus.Warn, *content, **kwargs)

    def error(self, *content, **kwargs):
        """
        错误日志
        :param content:内容
        :return:
        """
        self.template(LogStatus.Error, *content, **kwargs)

    def log_util(self, path_str, *content):
        """
        日志工具
        :param path_str:
        :param content:
        :return:
        """
        path = self.get_path(path_str)
        if self.save_flag:
            write(path, *content)

    def get_path(self, end_path):
        """
        日志类获取绝对路径
        :param end_path:
        :return:
        """
        _STATIC_TXT = os.path.join('', self.path + end_path)
        return _STATIC_TXT

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance


class logging(object):

    @classmethod
    def gen(cls, _object) -> ALog:
        return _object.log_obj
