import sys
import time


def sum_n(n):
    s = 0
    for i in range(n % 10):
        s += i
    for i in range(n % 10, n, 10):
        s += i
        s += (i + 1)
        s += (i + 2)
        s += (i + 3)
        s += (i + 4)
        s += (i + 5)
        s += (i + 6)
        s += (i + 7)
        s += (i + 8)
        s += (i + 9)
    return s


def main():
    argc = len(sys.argv)
    n = 10_000_000
    if argc > 1:
        n = int(sys.argv[1])

    start = time.time()

    num = sum_n(n)

    elapsed = time.time() - start

    print("Number:", num)
    print("Elapsed:", elapsed)


if __name__ == '__main__':
    main()
