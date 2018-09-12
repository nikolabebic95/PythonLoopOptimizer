import sys
import time


def lcg_random(seed, a, c, m, n):
    for i in range(n):
        seed = (a * seed + c) % m
    return seed


def main():
    argc = len(sys.argv)
    n = 10_000_000
    seed = 0
    a = 1664525
    c = 1013904223
    m = 2 ** 32
    if argc > 1:
        n = int(sys.argv[1])
    if argc > 2:
        seed = int(sys.argv[2])
    if argc > 3:
        a = int(sys.argv[3])
    if argc > 4:
        c = int(sys.argv[4])
    if argc > 5:
        m = int(sys.argv[5])

    start = time.time()

    num = lcg_random(seed, a, c, m, n)

    elapsed = time.time() - start

    print("Number:", num)
    print("Elapsed:", elapsed)


if __name__ == '__main__':
    main()
