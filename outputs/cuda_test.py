import numpy as np
from numba import guvectorize, float64
import math
from time import time


@guvectorize([(float64[:, :], float64[:, :])], '(n, m)->(n, m)')
def f(in_mat, out_mat):
    for i in range(len(in_mat)):
        for j in range(len(out_mat)):
            out_mat[i, j] = math.sin(in_mat[i, j])


def main():
    N = 1000
    in_mat = np.random.random((N, N))
    out_mat = np.empty((N, N), np.float64)

    start = time()

    f(in_mat, out_mat)

    end = time()
    print(end - start)


if __name__ == '__main__':
    main()
