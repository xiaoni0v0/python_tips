def gen():
    print('inner', g.gi_running)
    while True:
        yield


g = gen()

print(g.gi_running)
next(g)
print(g.gi_running)
