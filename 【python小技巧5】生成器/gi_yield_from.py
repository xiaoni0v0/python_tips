def gen():
    while True:
        yield from [0, 1, 2]


g = gen()

print(g.gi_yieldfrom)
print(next(g))
print(g.gi_yieldfrom)
