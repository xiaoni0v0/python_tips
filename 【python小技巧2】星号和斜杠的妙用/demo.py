import timeit


def f1():
    print(f'乘法：3 * 2 == {3 * 2}')
    print(f'乘方：3 ** 2 == {3 ** 2}')
    print(f'2 * 2 ** 2 ** 3 == {2 * 2 ** 2 ** 3}')


def f2():
    # x ** y     <==> pow(x, y)
    # x ** y % z <==> pow(x, y, z)
    def ff1():
        6 ** 6 ** 6 % 66

    def ff2():
        pow(6, pow(6, 6), 66)

    print(timeit.timeit(ff1, number=1000))
    print(timeit.timeit(ff2, number=1000))


def f3(a, /, b, *, c):
    print(a)
    print(b)
    print(c)


def add(x, y):
    return x + y


# arr = (4, 5)
# print(add(arr[0], arr[1]))
# print(add(*arr))
# #           ↓
# print(add(4, 5))

# dic = {'x': 4, 'y': 5}
# print(add(x=dic['x'], y=dic['y']))
# print(add(**dic))

def f4():
    a = (1, 5, 9, 6)
    b = (9, 8, 5, 3)
    print(a + b)
    print((*a, *b))
    #
    x = {'a': 1, 'b': 2}
    y = {'c': 3, 'd': 4}
    # print(x + y)
    print({**x, **y})


def f5():
    a, *_, c = (1, 2, 5, 6, 4, 7, 5)
    print(_)


def f6():
    print(f'除法(truediv 真除)：11 / 2 == {11 / 2}')
    print(f'整除：11 // 2 == {11 // 2}')


f6()
