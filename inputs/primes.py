def is_factor(a, b):
    return a % b == 0


def f(n):
    s = 0
    for i in range(2, n):
        for j in range(2, i):
            if is_factor(i, j):
                break
        else:
            s += 1
    return s


print(f(20000))
