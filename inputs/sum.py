import sys
import time


def sum_n(n):
    s = 0
    for i in range(n):
        s += i
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
