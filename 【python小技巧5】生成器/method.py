def gen_demo_close(v):
    print('生成器，启动！')
    try:
        yield v
    except GeneratorExit as e:
        print(repr(e))
        yield v + 1


def gen_demo_send(v):
    print('生成器，启动！')

    print('yield:', (yield v))
    print('yield:', (yield v))


def gen_demo_throw(v):
    print('生成器，启动！')

    # try:
    #     print('yield:', (yield v))
    # except Exception as e:
    #     print(e)

    print('yield:', (yield v))

    yield '结束'


g = gen_demo_throw(2)
