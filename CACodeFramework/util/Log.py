import binascii
import datetime
import os
import sys
import time
import warnings

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

    def __init__(self, path, print_flag=True, save_flag=True, max_clear=10240):
        """

        初始化配置

        :param path:保存的路径

        :param print_flag:是否打印日志 默认True

        :param save_flag:是否保存日志 默认True

        :param max_clear:日志储存最大限制,默认10MB 单位:KB

        """
        self.max_clear = max_clear
        self.path = path
        self.print_flag = print_flag
        self.save_flag = save_flag

    @staticmethod
    def log(obj, msg, line=sys._getframe().f_back.f_lineno, task_name='\t\tTask', LogObject=None):
        """
        输出任务执行日志

        :param obj:执行日志的对象地址
        :param msg:消息
        :param line:被调用前的行数
        :param task_name:任务对象的值
        :param LogObject:写出文件的对象

        """

        # 格式：时间 类型 日志名称 对象地址 被调用行号 执行类型 信息

        def str_to_hexStr(string):
            str_bin = string.encode('utf-8')
            return binascii.hexlify(str_bin).decode('utf-8')

        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        info = '[{}] [\t{}] [{}] [\t{}] [{}] [{}] \t\t\t:{}'.format(t,
                                                                    e_fields.INFO,
                                                                    e_fields.LOG_OPERA_NAME,
                                                                    id(obj),
                                                                    obj.__str__(),
                                                                    task_name,
                                                                    msg)
        # 输出日志信息
        warnings.warn_explicit(info, category=Warning, filename='line', lineno=line)
        if LogObject is not None:
            LogObject.warn(info)

        return info

    @staticmethod
    def err(cls, msg, LogObject=None):
        if LogObject is not None:
            LogObject.warn(msg)
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
        _log = '[%s]\t[%s] - %s\r\n' % (_date, 'content', str(content))
        if self.print_flag:
            print(_log)
        if self.save_flag:
            write(path, _log, self.max_clear)

    def get_path(self, end_path):
        """
        日志类获取绝对路径
        :param end_path:
        :return:
        """
        _STATIC_TXT = os.path.join('', self.path + end_path)
        return _STATIC_TXT
