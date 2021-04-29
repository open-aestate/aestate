import datetime
import os
import re
import sys
import threading
import time

from CACodeFramework.cacode.Modes import Singleton
from CACodeFramework.exception import e_fields


def date_format(time_obj=time, fmt='%Y-%m-%d %H:%M:%S'):
    """
    时间转字符串
    :param time_obj:
    :param fmt:
    :return:
    """
    _tm = time_obj.time()
    _t = time.localtime(_tm)
    return time.strftime(fmt, _t)


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
    def log(msg, obj=None, line=sys._getframe().f_back.f_lineno, task_name='\t\tTask', field=e_fields.Info(),
            LogObject=None, func_name="warn"):
        """
        输出任务执行日志

        :param obj:执行日志的对象地址
        :param msg:消息
        :param line:被调用前的行数
        :param task_name:任务对象的值
        :param field:日志级别
        :param LogObject:写出文件的对象

        """

        # 格式：时间 类型 日志名称 对象地址 被调用行号 执行类型 信息

        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # format(t,
        #        e_fields.Info(),
        #        e_fields.Log_Opera_Name(task_name),
        #        hex(id(obj)),
        #        obj.__str__(),
        #        task_name,
        #        msg)

        repr = re.findall(r'<.*>', obj.__repr__())[0]
        cc = repr[1:len(repr) - 1]
        repr_c = re.findall(r'<.*>', cc)
        if repr and not repr_c:
            write_repr = repr
        elif repr_c:
            write_repr = repr_c[0]
        else:
            write_repr = type(obj)
        # write_repr = repr if repr and not repr_c else repr_c[0] if repr_c else type(obj)
        info = f'[{t}] [\t{field}] [\t{line}] [{e_fields.Log_Opera_Name(task_name)}] [\t{hex(id(obj))}] [{write_repr}] ' \
               f'[{task_name}] \t\t\t:{msg}\n'
        # 输出日志信息
        file = sys.stderr
        file.write(info)
        # warnings.warn_explicit(info, category=Warning, filename='line', lineno=line)
        if LogObject is not None:
            # getattr(LogObject, func_name)(info)
            LogObject.warn(info)

        return info

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
        _date = date_format()
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
