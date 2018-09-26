import numpy as np
import math
from time import time


def main():
    n = 1000
    in_mat = np.random.random((n, n))
    out_mat = np.empty((n, n), np.float64)

    start = time()

    for i in range(len(in_mat)):
        for j in range(len(out_mat)):
            out_mat[i, j] = math.sin(in_mat[i, j])

    end = time()
    print(end - start)


if __name__ == '__main__':
    main()
