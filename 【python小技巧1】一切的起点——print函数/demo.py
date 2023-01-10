def f1():
    with open('./1.txt', 'w') as f:
        print('Hello World', file=f)
        print('Hello Python', file=f)


def f2():
    from io import StringIO

    s = StringIO()
    print('Hello World', file=s)
    print('Hello Python', file=s)

    print(s.getvalue())


def f3():
    with open('./1.txt', 'w') as f:
        print('Hello World', file=f, flush=True)
        input('...')
        print('Hello Python', file=f, flush=True)


if __name__ == '__main__':
    f3()
