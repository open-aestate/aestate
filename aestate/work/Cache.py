# -*- utf-8 -*-
import functools
import math
import os
import threading
import time
from collections import OrderedDict
from enum import Enum

import psutil

from aestate.exception import LogStatus
from aestate.util import others
from aestate.util.others import write, save_rb_tree
from aestate.work.Modes import Singleton

"""
全世界无产者,联合起来!!!
我们要强烈抵制资本主义的剥削!!!
"""


def tree_log(func):
    @functools.wraps(func)
    def function(a, b):
        save_rb_tree(a.root, "{}-{}".format(a.index, a.action))
        a.index += 1
        func(a, b)
        save_rb_tree(a.root, "{}-{}".format(a.index, a.action))
        a.index += 1

    return function


class CacheStatus(Enum):
    """
    缓存的状态
    """
    CLOSE = 0
    OPEN = 1


class SqlCacheItem(object):
    """缓存对象"""

    def __init__(self, key, value, instance):
        # 执行的sql
        self.sql = key
        # 长度,判断左右子树
        self.length = len(key)
        # 数据
        self.data = value
        self.instance = instance
        # 使用次数
        self.using_count = 0
        # 写入的时间
        self.create_time = time.time()
        self.last_using_time = time.time()
        # 左子树
        self.lchild = None
        # 右子树
        self.rchild = None
        # 删除标记, True为被删除,不会被搜索到
        self.is_delete = False
        # 平衡差,为左子树层级减去右子树层级，介于[-1,1]为合法值
        self.bf = 0
        super(SqlCacheItem, self).__init__()

    def __setattr__(self, key, value):
        if key == 'using_count':
            self.last_using_time = time.time()
        super(SqlCacheItem, self).__setattr__(key, value)

    def set_using_count(self):
        self.using_count += 1

    def get_sql(self):
        return self.sql

    def get_value(self):
        return self.data

    def set_value(self, value):
        self.data = value

    def is_black_node(self):
        return self.color == "B"

    def is_red_node(self):
        return self.color == "R"

    def set_black_node(self):
        self.color = "B"

    def set_red_node(self):
        self.color = "R"

    def print(self):
        if self.lchild:
            self.lchild.print()
        print(id(self))
        if self.rchild:
            self.rchild.print()


class DataContainer:
    """红黑树 数据容器"""

    def left_rotate(self, node):
        """
         * 左旋示意图：对节点x进行左旋
         *     parent               parent
         *    /                       /
         *   node                   right
         *  / \                     / \
         * ln  right   ----->     node  ry
         *    / \                 / \
         *   ly ry               ln ly
         * 左旋做了三件事：
         * 1. 将right的左子节点ly赋给node的右子节点,并将node赋给right左子节点ly的父节点(ly非空时)
         * 2. 将right的左子节点设为node，将node的父节点设为right
         * 3. 将node的父节点parent(非空时)赋给right的父节点，同时更新parent的子节点为right(左或右)
        :param node: 要左旋的节点
        :return:
        """
        parent = node.parent
        right = node.right
        # 把右子子点的左子点节   赋给右节点 步骤1
        node.right = right.left
        if node.right:
            node.right.parent = node
        # 把 node 变成基右子节点的左子节点 步骤2
        right.left = node
        node.parent = right
        # 右子节点的你节点更并行为原来节点的父节点。 步骤3
        right.parent = parent
        if not parent:
            self.root = right
        else:
            if parent.left == node:
                parent.left = right
            else:
                parent.right = right
        pass

    def right_rotate(self, node):
        """
         * 右旋示意图：对节点y进行右旋
         *        parent           parent
         *       /                   /
         *      node                left
         *     /    \               / \
         *    left  ry   ----->   ln  node
         *   / \                     / \
         * ln  rn                   rn ry
         * 右旋做了三件事：
         * 1. 将left的右子节点rn赋给node的左子节点,并将node赋给rn右子节点的父节点(left右子节点非空时)
         * 2. 将left的右子节点设为node，将node的父节点设为left
         * 3. 将node的父节点parent(非空时)赋给left的父节点，同时更新parent的子节点为left(左或右)
        :param node:
        :return:
        """
        parent = node.parent
        left = node.left

        # 处理步骤1
        node.left = left.right
        if node.left:
            node.left.parent = node

        # 处理步骤2
        left.right = node
        node.parent = left

        # 处理步骤3
        left.parent = parent
        if not parent:
            self.root = left
        else:
            if parent.left == node:
                parent.left = left
            else:
                parent.right = left
        pass

    def insert_node(self, node):
        """
        二叉树添加往红黑树中添加一个红色节点
        :param node:
        :return:
        """
        if not self.root:
            self.root = node
            return

        cur = self.root
        while cur:
            if cur.val < node.val:
                if not cur.right:
                    node.parent = cur
                    cur.right = node
                    break
                cur = cur.right
                continue

            if cur.val > node.val:
                if not cur.left:
                    node.parent = cur
                    cur.left = node
                    break
                cur = cur.left
        pass

    @tree_log
    def check_node(self, node):
        """
        检查节点及父节是否破坏了
        性质二：根节点是黑色；
        性质四：每个红色节点的两个子节点都是黑色的（也就是说不存在两个连续的红色节点）；
        @@ 性质四可反向理解为， 节点和其父点必定不能够同时为红色节点
        :param node:
        :return:
        """
        # 如果是父节点直接设置成黑色节点，退出
        if self.root == node or self.root == node.parent:
            self.root.set_black_node()
            print("set black ", node.val)
            return

        # 如果父节点是黑色节点，直接退出
        if node.parent.is_black_node():
            return

        # 如果父节点的兄弟节点也是红色节点,
        grand = node.parent.parent
        if not grand:
            self.check_node(node.parent)
            return
        if grand.left and grand.left.is_red_node() and grand.right and grand.right.is_red_node():
            grand.left.set_black_node()
            grand.right.set_black_node()
            grand.set_red_node()
            self.check_node(grand)
            return

        # 如果父节点的兄弟节点也是黑色节点,
        # node node.parent node.parent.parent 不同边
        parent = node.parent
        if parent.left == node and grand.right == node.parent:
            self.right_rotate(node.parent)
            self.check_node(parent)
            return
        if parent.right == node and grand.left == node.parent:
            parent = node.parent
            self.left_rotate(node.parent)
            self.check_node(parent)
            return

        # node node.parent node.parent.parent 同边
        parent.set_black_node()
        grand.set_red_node()
        if parent.left == node and grand.left == node.parent:
            self.right_rotate(grand)
            return
        if parent.right == node and grand.right == node.parent:
            self.left_rotate(grand)
            return

    def add_node(self, node):
        self.action = 'inser node {}'.format(node.val)
        self.insert_node(node)
        self.check_node(node)
        pass

    def check_delete_node(self, node):
        """
        检查删除节点node
        :param node:
        :return:
        """
        if self.root == node or node.is_red_node():
            return

        node_is_left = node.parent.left == node
        brother = node.parent.right if node_is_left else node.parent.left
        # brother 必不为空
        if brother.is_red_node():
            # 如果是黑色节点，兄弟节点是红色节点， 旋转父节点： 把你节点变成黑色，兄弟节点变黑色。 重新平衡
            if node_is_left:
                self.left_rotate(node.parent)
            else:
                self.right_rotate(node.parent)
            node.parent.set_red_node()
            brother.set_black_node()
            print("check node delete more ")
            # 再重新检查当前节点
            self.check_delete_node(node)
            return

        all_none = not brother.left and not brother.right
        all_black = brother.left and brother.right and brother.left.is_black_node() and brother.right.is_black_node()
        if all_none or all_black:
            brother.set_red_node()
            if node.parent.is_red_node():
                node.parent.set_black_node()
                return
            self.check_delete_node(node.parent)
            return

        # 检查兄弟节点的同则子节点存丰并且是是红色节点
        brother_same_right_red = node_is_left and brother.right and brother.right.is_red_node()
        brother_same_left_red = not node_is_left and brother.left and brother.left.is_red_node()
        if brother_same_right_red or brother_same_left_red:

            if node.parent.is_red_node():
                brother.set_red_node()
            else:
                brother.set_black_node()
            node.parent.set_black_node()

            if brother_same_right_red:
                brother.right.set_black_node()
                self.left_rotate(node.parent)
            else:
                brother.left.set_black_node()
                self.right_rotate(node.parent)

            return

        # 检查兄弟节点的异则子节点存丰并且是是红色节点
        brother_diff_right_red = not node_is_left and brother.right and brother.right.is_red_node()
        brother_diff_left_red = node_is_left and brother.left and brother.left.is_red_node()
        if brother_diff_right_red or brother_diff_left_red:
            brother.set_red_node()
            if brother_diff_right_red:
                brother.right.set_black_node()
                self.left_rotate(brother)
            else:
                brother.left.set_black_node()
                self.right_rotate(brother)

            self.check_delete_node(node)
            return

    def pre_delete_node(self, node):
        """
        删除前检查，返回最终要删除的点
        :param node:
        :return:
        """
        post_node = self.get_post_node(node)
        if post_node:
            node.val, post_node.val = post_node.val, node.val
            return self.pre_delete_node(post_node)
        pre_node = self.get_pre_node(node)
        if pre_node:
            pre_node.val, node.val = node.val, pre_node.val
            return self.pre_delete_node(pre_node)
        # 没有前驱节点，也没有后续节点
        return node

    def get_pre_node(self, node):
        """
        获取 前驱 节点 ， 树中比node小的节点中最大的值
        :param node:
        :return:
        """
        if not node.left:
            return None
        pre_node = node.left
        while pre_node.right:
            pre_node = pre_node.right
        return pre_node

    def get_post_node(self, node):
        """
        获取后续节点:
        :param node:树中比node大的节点中最小的值
        :return:
        """
        if not node.right:
            return None
        post_node = node.right
        while post_node.left:
            post_node = post_node.left
        return post_node

    def get_node(self, val):
        """
        根据值查询节点信息
        :param val:
        :return:
        """
        if not self.root:
            return None
        node = self.root
        while node:
            if node.val == val:
                break
            if node.val > val:
                node = node.left
                continue
            else:
                node = node.right
        return node

    def delete_node(self, val):

        node = self.get_node(val)
        if not node:
            print("node error {}".format(val))
            return
        save_rb_tree(self.root, "{}_delete_0".format(val))
        # 获取真正要删除的节点
        node = self.pre_delete_node(node)
        save_rb_tree(self.root, "{}_delete_1".format(val))
        # node 节点必不为空，且子节点也都为空
        self.check_delete_node(node)
        save_rb_tree(self.root, "{}_delete_2".format(val))
        # 真正删除要删除的节点
        self.real_delete_node(node)
        save_rb_tree(self.root, "{}_delete_3".format(val))
        pass

    def real_delete_node(self, node):
        """
        真正删除节点函数
        :param node:
        :return:
        """
        if self.root == node:
            self.root = None
            return
        if node.parent.left == node:
            node.parent.left = None
            return
        if node.parent.right == node:
            node.parent.right = None
        return

    # -----------------------

    @staticmethod
    def left_whirl(node):
        """
        左旋
        当node值为-2的时候可以执行此操作使其节点值为0,node为最小不平衡树的根节点
        :param node:
        :return:
        """
        node.bf = node.rchild.bf = 0

        node_right = node.rchild
        node.rchild = node.rchild.lchild
        node_right.lchild = node
        return node_right

    @staticmethod
    def right_whirl(node):
        """
        右旋
        当node值为2的时候可以执行此操作使其节点值为0,node为最小不平衡树的根节点
        :param node:
        :return:
        """
        node.bf = node.lchild.bf = 0
        node_left = node.lchild
        node.lchild = node.lchild.rchild
        node_left.rchild = node
        return node_left

    @staticmethod
    def left_right_whirl(node):
        """
        左右旋,先左旋子节点,再右旋node节点
        :param node:
        :return:
        """
        node_b = node.lchild
        node_c = node_b.rchild
        node.lchild = node_c.rchild
        node_b.rchild = node_c.lchild
        node_c.lchild = node_b

        node_c.rchild = node

        if node_c.bf == 0:
            node.bf = node_b.bf = 0
        elif node_c.bf == 1:
            node.bf = -1
            node_b.bf = 0
        else:
            node.bf = 0
            node_b.bf = 1

        node_c.bf = 0
        return node_c

    @staticmethod
    def right_left_whirl(node):
        """
        右左旋,先右旋子节点,再左旋node节点
        :param node:
        :return:
        """
        node_b = node.rchild
        node_c = node_b.lchild

        node_b.lchild = node_c.rchild
        node.rchild = node_c.lchild
        node_c.rchild = node_b

        node_c.lchild = node

        if node_c.bf == 0:
            node.bf = node_b.bf = 0
        elif node_c.bf == 1:
            node.bf = 0
            node_b.bf = -1
        else:
            node.bf = 1
            node_b.bf = 0

        node_c.bf = 0
        return node_c

    def __init__(self):
        self.root = None
        self.index = 1
        self.action = ""

    def _search(self, key: str) -> SqlCacheItem or None:
        temp = self.root
        while temp:
            if temp.length == len(key) and temp.get_sql() == key:
                if temp.is_delete:
                    temp = None
                break
            elif temp.length > len(key):
                temp = temp.lchild
            else:
                temp = temp.rchild
        else:
            return None

        return temp

    def search(self, key):
        res = self._search(key)
        if res:
            return res
        return None

    def insert(self, targetNode: SqlCacheItem):
        key, value = targetNode.length, targetNode.data
        if not self.root:
            self.root = targetNode
            return
        mut_node, point = self.root, self.root
        mut_parent, p_parent = None, None
        while point:
            if point.length == key and point.get_sql() == targetNode.get_sql():
                point.set_value(value)
                return
            if point.bf != 0:
                mut_parent, mut_node = p_parent, point
            p_parent = point
            if key > point.length:
                point = point.rchild
            else:
                point = point.lchild
        if key > p_parent.length:
            p_parent.rchild = targetNode
        else:
            p_parent.lchild = targetNode
        ta = mut_node
        while ta:
            if ta.length == key:
                break
            elif key > ta.length:
                ta.bf -= 1
                ta = ta.rchild
            else:
                ta.bf += 1
                ta = ta.lchild
        if mut_node.length > key:
            if mut_node.lchild:
                p_pos = mut_node.lchild.length > key
            else:
                mut_node.lchild = targetNode
                p_pos = False
        else:
            if mut_node.rchild:
                p_pos = mut_node.rchild.length > key
            else:
                mut_node.rchild = targetNode
                p_pos = False
        if mut_node.bf > 1:
            if p_pos:
                mut_node = DataContainer.right_whirl(mut_node)
            else:
                mut_node = DataContainer.left_right_whirl(mut_node)
        elif mut_node.bf < -1:
            if p_pos:
                mut_node = DataContainer.right_left_whirl(mut_node)
            else:
                mut_node = DataContainer.left_whirl(mut_node)
        if mut_parent:
            if mut_parent.length > key:
                mut_parent.lchild = mut_node
            else:
                mut_parent.rchild = mut_node
        else:
            self.root = mut_node

    def delete(self, key):
        """
        删除节点并返回该节点的值
        :return:
        """
        p = self._search(key)
        if not p:
            return False
        p.is_delete = True
        return p.get_value()


class SqlCacheManage(object):
    """
    缓存管理

    1.当内存满足系统运行内存的1/10时,满足最大限度数据内容,保证数据完整性的同时保留数据

    2.当单次查询数据大于阈值时,保留数据并不在扩大缓存空间,数据完整保留,但不再清理,直到处于第二缓存空间更多查询数据量再次大于阈值时清理

    3.当通过aestate改变数据时记录数据变更信息,并重新将数据写入缓存,移除旧缓存数据,这将意味着非通过aestate修改的数据不可被检测到

    4.扩容策略:当前内存>=当前容量1/2时,重新计算查询数据量

    5.流量计算方式:当前缓存大小 + (当前缓存大小 / 上次扩容时间至当前时间段内插入的新内容数量) ** 2

    6.移除方案:时间段内缓存查询次数最少内存最大优先,当 (A次数-B次数) * 10 <= (A占用内存-B占用内存),优先删除B
    """
    # 初始内存大小为1024Byte
    __capacity_max__ = 1024
    # 系统运行时计算得到的内存阈值
    __max__ = psutil.virtual_memory().free / 10
    _instance_lock = threading.RLock()
    # 容器
    data_container = DataContainer()
    # 缓存的状态
    status = CacheStatus.OPEN

    def __contains__(self, o: str) -> bool:
        """判断缓存中是否存在这个sql的查询记录"""
        return self.data_container.search(o)

    def get_size(self):
        """获取当前缓存的大小"""
        return self.get_container_size()

    def get_max(self):
        return self.__max__

    def need_calculate(self):
        """是否需要清理缓存"""
        return self.get_capacity_max() / 2 <= self.get_size()

    def calculate_ram(self) -> bool:
        """扩容"""
        self.reset_max_ram()
        if self.need_calculate():
            target_ram = int(self.get_capacity_max() * 2 + self.get_size())
            if target_ram < self.get_max():
                self.__capacity_max__ = target_ram
                return True
            else:
                # 直接等于最大内存,然后清理一下
                self.__capacity_max__ = self.get_max()
                # 当前允许的最大内存的20%(缓存的平均值),直到缓存满足
                size = math.ceil((self.get_capacity_max() * 0.2) / (self.get_size() / len(self.data_container)))
                if size != 0:
                    while size:
                        del self.data_container[0]
                        size -= 1
                return True
        else:
            return False

    def get(self, sql) -> SqlCacheItem:
        """获取一条sql"""
        target = self.index(sql)
        target.set_using_count()
        return target

    def remove(self, sql):
        """移除某个sql的缓存"""
        index = self.index(sql)
        if index != -1:
            del self.data_container[index]

    def remove_by_instance(self, tb_name):
        """根据instance的表来删除缓存"""
        self.data_container.delete(tb_name)

    def clean_up(self):
        """清理缓存,不是清除缓存,清理是清理使用次数不多的缓存"""
        if self.need_calculate():
            # 先试图扩容
            self.calculate_ram()

    def reset_max_ram(self):
        """重新计算当前可用的最大缓存"""
        free_ram = psutil.virtual_memory().free
        self.__max__ = int(free_ram / 10)

    def set(self, sql, value, instance):
        self.data_container.insert(targetNode=SqlCacheItem(key=sql, value=value, instance=instance))
        # 判断缓存是否已经满了
        self.clean_up()

    def get_container(self) -> DataContainer:
        return self.data_container

    def get_container_size(self):
        return self.data_container.__sizeof__()

    def get_capacity_max(self):
        """获取当前内存允许的最大限制"""
        return self.__capacity_max__

    def clear(self):
        """清空缓存,谨慎操作
        如果仅仅是需要清理缓存空间,请使用clean_up()函数
        """
        self.data_container.root = None

    def index(self, sql):
        """验证sql是否存在缓存"""
        return self.data_container.search(sql)

    def __new__(cls, *args, **kwargs):
        """
        单例管理缓存内容
        """
        instance = Singleton.createObject(cls)
        return instance


class PojoContainer:
    """对象管理器"""

    def __init__(self):
        self.solvent = []

    def __add__(self, __object):
        self.solvent.append(__object)

    @property
    def size(self) -> int:
        return len(self.solvent)

    def get(self, name):
        for item in self.solvent:
            if item._type == name:
                return item._object
        return None


class PojoItemCache(OrderedDict):
    """单个对象的容器"""

    def __init__(self, _type, _object):
        super(PojoItemCache).__init__()
        self._type = _type
        self._object = _object


class PojoManage:
    """管理pojo的缓存"""
    _instance_lock = threading.RLock()
    pojo_list = PojoContainer()

    def append(self, _cls_name: type, _object):
        self.pojo_list + PojoItemCache(_type=_cls_name, _object=_object)

    @staticmethod
    def get(_cls, *args, **kwargs):
        if 'new' in kwargs.keys() and kwargs['new'] == True:
            return object.__new__(_cls)
        this = PojoManage()
        _class_object_ = object.__new__(_cls)
        cls_name = others.fullname(_class_object_)
        _obj = this.pojo_list.get(cls_name)
        if _obj is None:
            this.append(cls_name, _class_object_)
            _obj = this.pojo_list.get(cls_name)
        [setattr(_obj, k, v) for k, v in kwargs.items()]
        return _obj

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance


class LogCache:
    _instance_lock = threading.RLock()
    # 是否已经显示logo了
    info_logo_show = False
    warn_logo_show = False
    error_logo_show = False
    # 文件名,当满足最大时将会使用一个新的文件作为储存日志
    info_file_name = []
    warn_file_name = []
    error_file_name = []

    def get_filename(self, path, max_clear, status):

        if status == LogStatus.Info:
            center_name = 'info'
            oa = self.info_file_name
            logo_show = 'info_logo_show'
        elif status == LogStatus.Error:
            center_name = 'error'
            oa = self.warn_file_name
            logo_show = 'error_logo_show'
        elif status == LogStatus.Warn:
            center_name = 'warn'
            oa = self.error_file_name
            logo_show = 'warn_logo_show'
        else:
            center_name = 'info'
            oa = self.info_file_name
            logo_show = 'info_logo_show'

        _path = os.path.join(path, center_name)
        if len(oa) == 0:
            oa.append(others.date_format(fmt='%Y.%m.%d.%H.%M.%S') + '.log')
            setattr(self, logo_show, False)
        else:
            if not os.path.exists(os.path.join(_path, oa[len(oa) - 1])):
                write(os.path.join(_path, '.temp'), '')
                setattr(self, logo_show, False)
            if os.path.getsize(os.path.join(_path, oa[len(oa) - 1])) >= max_clear:
                oa.append(others.date_format(fmt='%Y.%m.%d.%H.%M.%S') + '.log')
                setattr(self, logo_show, False)

        return os.path.join(center_name, oa[len(oa) - 1])

    def __new__(cls, *args, **kwargs):
        instance = Singleton.createObject(cls)
        return instance
