# -*- utf-8 -*-
# @Time: 2021/6/27 15:11
# @Author: CACode
# 大任务
import time

from aestate.util._thread import ThreadPool, ThreadTask


# 大任务
def big_job(arg):
    print(arg)
    global end1, end2, end3
    for i in range(0, 10000):
        a = 9 * 9
    if arg[0] == 9:
        if arg[1] == 1:
            end1 = time.clock()
        if arg[1] == 2:
            end2 = time.clock()
        if arg[1] == 3:
            end3 = time.clock()


# 小任务
def small_job(arg):
    global end1, end2, end3
    print(arg)
    a = 9 * 9
    if arg[0] == 9:
        if arg[1] == 1:
            end1 = time.clock()
        if arg[1] == 2:
            end2 = time.clock()
        if arg[1] == 3:
            end3 = time.clock()


end1 = 0
end2 = 0
end3 = 0

if __name__ == '__main__':
    begin1 = time.clock()
    tp = ThreadPool(5)
    for x in range(0, 10):
        new_job = ThreadTask(big_job, [x, 1])
        tp.add_task(new_job)
    del tp

    begin2 = time.clock()
    tp = ThreadPool(100)
    for x in range(0, 10):
        new_job = ThreadTask(small_job, [x, 2])
        tp.add_task(new_job)
    del tp

    begin3 = time.clock()
    for x in range(0, 10):
        small_job([x, 3])
    # 防止主线程先跑完
    while end1 == 0 or end2 == 0 or end3 == 0:
        pass
    print('5 thread used ' + str(end1 - begin1))
    print('100 thread used ' + str(end2 - begin2))
    print('1 thread used ' + str(end3 - begin3))
