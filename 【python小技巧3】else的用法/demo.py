import os


def f1():
    3 / 0
    # xxx

    print(1)
    return 1


def f2():
    print(2)
    return 2


def f3():
    cond = False
    res = f1() if cond else f2()


def f4():
    try:
        # int('x')
        int('3')
        return
    except ValueError:
        print('ValueError')
    except Exception:
        print('Exception')
    else:
        print('else')
    finally:
        print('finally')


def f5():
    try:
        int('x')
    finally:
        print('finally')


def f6():
    try:
        exit()
        # raise SystemExit
    except Exception:
        print('except')

    print('after')


def f7():
    try:
        os._exit(0)
    except Exception:
        print('except')
    finally:
        print('finally')


f7()
