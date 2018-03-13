import time
import random
N = 10000000
lst = []


def helper(s, elem):
    s += elem
    s %= 100
    return s


def init():
    i = 0
    while i < N:
        lst.append(random.random())
        i = i + 1


def f():
    s = 0
    for elem in lst:
        s = helper(s, elem)


def inlined():
    s = 0
    for elem in lst:
        s += elem
        s %= 100


init()
start_time = time.time()
f()
print("Elapsed time: ", time.time() - start_time, " seconds")
start_time = time.time()
inlined()
print("Inlined:      ", time.time() - start_time, " seconds")
