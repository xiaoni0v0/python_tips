def get_iterator(s: str):
    print(s)
    return iter([0, 1, 2])


a = (x for x in get_iterator('first') if x for i in get_iterator('second'))

print((x for x in range(3)))

# print(x for x in range(3), 1)
