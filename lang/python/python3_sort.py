import functools
a = range(1, 11)
a = list(a)

a.sort(key=functools.cmp_to_key(lambda x, y: -1 if x % 2> y %2 else x < y ))
print(a)