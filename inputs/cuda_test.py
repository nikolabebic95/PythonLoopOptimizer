import numpy as np
import math
from time import time


def main():
    n = 1000
    in_mat = np.random.random((n, n))
    out_mat = np.empty((n, n), np.float64)

    start = time()

    for i in range(in_mat.shape[0]):
        for j in range(in_mat.shape[1]):
            out_mat[i, j] = math.sin(in_mat[i, j])

    end = time()
    print(end - start)


if __name__ == '__main__':
    main()
