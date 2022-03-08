# -*- utf-8 -*-
# @Time: 2021/5/30 10:17
# @Author: CACode
import os
import time
from datetime import datetime

from aestate.conf import BASE_ATTR

try:
    import matplotlib.pyplot as plt
except:
    pass


def conversion_types(val):
    """
    将val的类型转换为字符串并插入array
    """
    if isinstance(val, datetime):
        val = val.strftime('%Y-%m-%d %H:%M:%S')
    return val


def date_format(time_obj=time, fmt='%Y-%m-%d %H:%M:%S') -> str:
    """
    时间转字符串
    :param time_obj:
    :param fmt:
    :return:
    """
    _tm = time_obj.time()
    _t = time.localtime(_tm)
    return time.strftime(fmt, _t)


def time_to_datetime(t_time):
    """
    时间戳转datetime
    """
    try:
        d_time = datetime.fromtimestamp(t_time)
    except OSError as ose:
        return None
    return d_time


def get_static_fields(cls):
    """
    获取类的非默认全局变量
    """
    retD = list(set(dir(cls)).difference(set(BASE_ATTR)))
    return retD


def fullname(o):
    """获取对象的类名"""
    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        cls_name = o.__class__.__name__
    else:
        cls_name = module + '.' + o.__class__.__name__

    if cls_name == 'type':
        cls_name = o.__base__.__module__ + '.' + o.__base__.__name__

    return cls_name


def logTupleToText(next_line=True, *content):
    temp = []
    if isinstance(content, str):
        temp.append(content)
    elif isinstance(content, tuple):
        for c in content:
            if isinstance(c, tuple):
                temp.extend(c)
            else:
                temp.append(str(c))
    else:
        temp.append(str(content))
    if next_line:
        temp.append('\n')
    return ''.join([str(_) for _ in temp])


def write(path, *content):
    """
    写出文件
    :param path:位置
    :param content:内容
    :return:
    """
    # 防止有些使用`/`有些用`\\`
    _sep_path = []
    s = path.split('/')
    [_sep_path.extend(item.split('\\')) for item in s]
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
    _write_content = logTupleToText(True, *content)
    with open(os.path.join(_path), mode="a", encoding="UTF-8") as f:
        f.write(_write_content)
        f.close()


def get_left_length(node):
    if not node:
        return 0
    if not node.left:
        return 1
    if not node.right:
        return 2 + get_left_length(node.right)
    return 2 + get_left_length(node.left)


def get_right_length(node):
    if not node:
        return 0
    return 1 + get_right_length(node.right)


def get_height(node):
    if not node:
        return 0
    return 1 + max([get_height(node.left), get_height(node.right)])


def get_node_count(node):
    if not node:
        return 0
    return 1 + get_node_count(node.left) + get_node_count(node.right)


def get_fontsize(count):
    if count < 10:
        return 30
    if count < 20:
        return 20
    return 16


def show_node(node, ax, height, index, font_size):
    if not node:
        return
    x1, y1 = None, None
    if node.left:
        x1, y1, index = show_node(node.left, ax, height - 1, index, font_size)
    x = 100 * index - 50
    y = 100 * height - 50
    if x1:
        plt.plot((x1, x), (y1, y), linewidth=2.0, color='b')
    circle_color = "black" if node.is_black_node() else 'r'
    text_color = "beige" if node.is_black_node() else 'black'
    ax.add_artist(plt.Circle((x, y), 50, color=circle_color))
    ax.add_artist(plt.Text(x, y, node.val, color=text_color, fontsize=font_size, horizontalalignment="center",
                           verticalalignment="center"))
    # print(str(node.val), (height, index))

    index += 1
    if node.right:
        x1, y1, index = show_node(node.right, ax, height - 1, index, font_size)
        plt.plot((x1, x), (y1, y), linewidth=2.0, color='b')

    return x, y, index


def draw_node_line(node, ax, height, index):
    x1, y1 = None, None
    if node.left:
        x1, y1, index = draw_node_line(node.left, ax, height - 1, index)
    x = 100 * index - 50
    y = 100 * height - 50
    if x1:
        plt.plot((x1, x), (y1, y), linewidth=2.0, color='b')
    index += 1
    if node.right:
        x1, y1, index = draw_node_line(node.right, ax, height - 1, index)
        plt.plot((x1, x), (y1, y), linewidth=2.0, color='b')

    return x, y, index


def show_rb_tree(tree, title):
    fig, ax = plt.subplots()
    left, right, height = get_left_length(tree), get_right_length(tree), get_height(tree)
    # print(left, right, height)
    plt.ylim(0, height * 100 + 100)
    plt.xlim(0, 100 * get_node_count(tree) + 100)
    show_node(tree, ax, height, 1)
    plt.show()


def save_rb_tree(tree, index):
    fig, ax = plt.subplots()
    fig.set_facecolor('gray')
    left, right, height = get_left_length(tree), get_right_length(tree), get_height(tree)
    # print(left, right, height)
    h = height * 100 + 100
    w = 100 * get_node_count(tree) + 100
    if w < 400:
        w = 400
        h = h * 400 / w
    plt.text(w / 2 - 50, h - 40, index, size=30, family="fantasy", color="r",
             style="italic", weight="light", bbox=dict(facecolor="r", alpha=0.2))
    plt.ylim(0, h)
    plt.xlim(0, w)
    show_node(tree, ax, height, 1, get_fontsize(get_node_count(tree)))

    fig.set_size_inches(10, h / (w / 10))
    plt.savefig("rb/rbtree_{}.png".format(index))


def dp_equals_base(cls, base_cls):
    """
    寻找是否属于cls的基类
    :param cls:
    :param base_cls:
    :return:
    """
    # if cls.__class__
    if cls is None:
        return False
    if cls.__base__ != type:
        if cls.__base__ == base_cls:
            return True
        else:
            return dp_equals_base(cls.__base__, base_cls)
    else:
        return False
