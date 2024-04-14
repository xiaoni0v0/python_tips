from collections.abc import Generator, Iterator, Iterable
from dis import dis


def common_func(arg):
    print('Input:', arg)

    return None


def does_any_func_has_ret():
    def f1():
        print()

    def f2():
        print()
        return None

    def f3():
        print()
        return

    print(f1)
    dis(f1)
    print(f2)
    dis(f2)
    print(f3)
    dis(f3)


def gen_func(arg):
    print('Input:', arg)

    yield arg + 1
    print('1')
    yield arg + 2
    print('2')
    yield arg + 3
    print('3')

    return '函数结束'


def using_gen_func():
    a = gen_func(2)

    # next(a)
    # next(a)
    # next(a)
    #
    # try:
    #     next(a)
    # except StopIteration as e:
    #     print(e.value)

    print(isinstance(a, Iterator))
    print(isinstance(a, Iterable))

    print(isinstance(a, Generator))

    print(iter(a) is a)


def method_and_property_of_gen():
    a = gen_func(2)
    b = iter([])

    print(set(dir(a)) - set(dir(b)))

    # print('gi_code:', a.gi_code)
    # print('gi_frame:', a.gi_frame)
    # print('gi_running:', a.gi_running)
    # print('gi_yieldfrom:', a.gi_yieldfrom)


def list_comprehension():
    l = []
    for x in range(10):
        if x % 3 == 0:
            for i in range(3):
                l.append(x)

    return (x for x in range(10) if x % 3 == 0 for i in range(3))
