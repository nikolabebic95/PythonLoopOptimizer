def f(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    s = 0
    for i in range(n):
        s += f(i)
    return s


print(f(10))
