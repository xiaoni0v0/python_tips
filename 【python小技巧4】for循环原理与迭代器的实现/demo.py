"""
【python小技巧4】for循环原理与迭代器的实现

本期内容：

1. 讲述 for 循环的具体工作原理：
    第一种情况: __iter__() 后 __next__()
    第二种情况: __getitem__()
2. 怎样实现迭代器

作者：B站 小倪同学0v0

创建于 2023/1/13
"""

from collections.abc import Iterable, Iterator


def f1():
    for i in '', [], (), {}, set():
        print('%s: \t%s %s' % (repr(i), isinstance(i, Iterable), isinstance(i, Iterator)))


class Names:
    def __init__(self):
        self.lst = []

    def add(self, n):
        self.lst.append(n)

    def __iter__(self):
        return NamesIterator(self)


class NamesIterator:
    def __init__(self, obj: 'Names'):
        self.obj = obj
        self.index = 0

    def __next__(self):
        if self.index < len(self.obj.lst):
            temp = self.obj.lst[self.index]
            self.index += 1
            return temp
        else:
            raise StopIteration


class Names2:
    def __init__(self):
        self.lst = []

    def add(self, n):
        self.lst.append(n)

    def __iter__(self):
        index = 0
        while index < len(self.lst):
            yield self.lst[index]
            index += 1


names = Names2()
names.add('张三')
names.add('李四')
names.add('王五')
names.add('王八')


def f2():
    for i in names:
        print(i)


def f3():
    for i in names:
        for j in names:
            print(i, j)


f3()
