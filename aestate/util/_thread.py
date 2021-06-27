# -*- utf-8 -*-
# @Time: 2021/6/27 15:06
# @Author: CACode
import threading


# 线程池的任务，包含一个可调用对象和一个参数数组
class ThreadTask(object):
    def __init__(self, job, *args, **kwargs):
        if args is None:
            args = list()
        self.task = job
        self.args = args
        self.kwargs = kwargs


# 线程池对象
class ThreadPool(object):
    def __init__(self, thread_length):
        self.task_list = list()
        self.task_lock = threading.RLock()
        self.task_condition = threading.Condition()
        self.thread_length = thread_length
        self.thread_list = list()
        for i in range(0, thread_length):
            self.thread_list.append(threading.Thread(name='Thread ' + str(i), target=ThreadPool.thread_work,
                                                     args=[self]))
        for thread in self.thread_list:
            thread.start()

    # 在加锁的情况下添加任务，如果任务队列为空，就发出一个信号，唤醒所有线程
    def add_task(self, new_task):
        self.task_lock.acquire()
        if len(self.task_list) == 1:
            self.task_condition.acquire()
            self.task_condition.notifyAll()
            self.task_condition.release()
        self.task_list.append(new_task)
        self.task_lock.release()
        return True

    # 每个线程的主函数，每个线程都不断地读取任务队列，有任务时执行任务，没有时自己睡眠

    def thread_work(self):
        while True:
            self.task_lock.acquire()
            if len(self.task_list) == 0:
                self.task_lock.release()
                self.task_condition.acquire()
                self.task_condition.wait()
                self.task_condition.release()
            else:
                temp_task = self.task_list.pop()
                self.task_lock.release()
                temp_task.task(temp_task.args)
