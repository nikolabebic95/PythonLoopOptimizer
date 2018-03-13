import random
N = 10000000


def f():
    i = 0
    s = 0
    while i < N:
        s += random.random()
        s %= 100
        i = i + 1


f()
