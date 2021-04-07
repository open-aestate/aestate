# 使用控制台制作2048小游戏


import random


class Game(object):

    def __init__(self):
        self.len1 = 4
        self.list1 = [0] * self.len1

        for i in range(self.len1):
            row = [0] * self.len1
            self.list1[i] = row
        self.random1()
        self.random1()

        self.score = 0
        self.key1 = ""

    def show(self):
        print("—————————")
        for i in self.list1:
            for a in i:
                num1 = len(i)
                str1 = ""
                while num1 >= len(str(a)):
                    str1 += " "
                    num1 -= 1
                print(str(a) + "", end=str1)
            print("")
        print("—————————当前分数：" + str(self.score))

    def key(self):
        self.key1 = input("请输入w a s d操作棋盘")
        if self.key1 == "w" or self.key1 == "s" or self.key1 == "a" or self.key1 == "d":
            self.f()
            self.move()
            self.f()
            self.main()
        else:
            print("请输入小写字母w a s d操作")
            self.key1 = None
            self.key()

    def remove_l1(self):
        for i in range(len(self.list1) - 1):
            for j in range(len(self.list1[i]) - 1):
                if self.list1[i][j] == 0:
                    self.list1[i].pop(j)

    def f(self):  # 将数组重新排序

        l1 = [0] * self.len1
        if self.key1 == "w":
            for i in range(self.len1):
                row = [0] * self.len1
                for j in range(self.len1):
                    row[j] = self.list1[j][i]
                l1[i] = row
        elif self.key1 == "s":
            for i in range(self.len1):
                row = [0] * self.len1
                for j in range(self.len1):
                    row[j] = self.list1[j][i]
                row.reverse()
                l1[i] = row
            l1.reverse()
        elif self.key1 == "a":
            for i in range(self.len1):
                row = [0] * self.len1
                for j in range(self.len1):
                    row[j] = self.list1[i][j]
                l1[i] = row
        elif self.key1 == "d":
            for i in range(self.len1):
                row = [0] * self.len1
                for j in range(self.len1):
                    row[j] = self.list1[i][j]
                row.reverse()
                l1[i] = row
            l1.reverse()

        self.list1 = l1

    def move(self):
        # 真是个可怕的BUG(其实是python的特性)，从浅拷贝到指针，数组间的内存地址指向。。
        # 存储尚未移动的数组用作比较
        dbl = [0] * self.len1
        num5 = 0
        for i in self.list1:
            num6 = 0
            row2 = [0] * self.len1
            for j in i:
                row2[num6] = j
                num6 += 1
            dbl[num5] = row2
            num5 += 1
        # （清除每行数组中的0）
        i = 0
        while i < len(self.list1):
            j = 0
            while j < len(self.list1[i]):
                if self.list1[i][j] == 0:
                    self.list1[i].pop(j)
                    j -= 1
                j += 1
            i += 1

        # 移动数组位置
        num3 = 0
        for row in self.list1:
            # print(row) 用来调试的
            l1 = []
            num1 = 0  # 迭代值
            while num1 <= len(row) - 1:
                if num1 == len(row) - 1:
                    l1.append(row[num1])
                    num1 += 1
                else:
                    if row[num1] == row[num1 + 1]:
                        l1.append((row[num1] + row[num1 + 1]))
                        self.score += (row[num1] + row[num1 + 1])

                        num1 += 2
                    else:
                        l1.append(row[num1])
                        num1 += 1
            # 判断是否有得到新的数
            if len(l1) > 0:
                self.list1[num3] = l1
            # 为数组重新补位0
            while 1 == 1:

                if len(self.list1[num3]) < self.len1:
                    self.list1[num3].append(0)
                else:
                    break
            num3 += 1

        if dbl != self.list1:
            self.random1()
        else:
            print("您没有让棋盘改变")

    def random1(self):
        num1 = 0
        while num1 <= 0:
            for i in range(len(self.list1) - 1):
                for j in range(len(self.list1[i]) - 1):

                    if self.list1[i][j] == 0:
                        if num1 == 0:
                            self.list1[i][j] = random.choice([0, 0, 0, 0, 2, 4])

                            # print("略过了一个数")用来调试
                        if self.list1[i][j] > 0:
                            num1 += 1
                            # print("随机数生成完毕！")用来调试
                            break

    def main(self):
        num1 = 0
        for i in range(len(self.list1) - 1):
            for j in range(len(self.list1[i]) - 1):
                if self.list1[i][j] > 0:
                    num1 += 1

        if num1 < (self.len1 * self.len1):
            self.show()
            self.key()

        else:
            print("棋盘被填满了，你的最终分数：" + str(self.score))


def run():
    """
    开启彩蛋小游戏
    """
    p1 = Game()
    p1.main()


if __name__ == '__main__':
    print('CACode小彩蛋', '感谢作者提供：https://gitee.com/HelloBugWorld/2048')
    run()
