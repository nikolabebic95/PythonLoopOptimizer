def f(n):
    s = 0
    for i in range(2, n):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            s += 1
    return s


f(20000)
