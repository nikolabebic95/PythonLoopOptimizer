n = 53
abc = 10
xxx = 10


def f(a, x, y, z):
    global n, abc
    b = a
    b = 10
    n = 35
    lst = [2]
    lst[0] = 1
    for j in lst:
        pass
    return b


while abc < n:
    a = 10
    b = 10
    c = 1 + 2 + f(a + 1, 2, 3, 4)
    print(n)
    abc = 1000
