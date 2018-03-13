import time
import random
import numpy

N = 10000000
lst = []


def init():
    i = 0
    while i < N:
        lst.append(random.random())
        i = i + 1
    return numpy.array(lst)


def f():
    s = 0
    for elem in lst:
        s += elem
        s %= 100


def optimized():
    s = 0
    for elem in arr:
        s += elem
        s %= 100


arr = init()
start_time = time.time()
f()
print("Elapsed time: ", time.time() - start_time, " seconds")
start_time = time.time()
optimized()
print("Numpy:        ", time.time() - start_time, " seconds")
