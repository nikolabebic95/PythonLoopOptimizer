import numba
import numpy as np
import math
from time import time


# comment
@numba.guvectorize([(numba.float64[:, :], numba.float64[:, :])], '(n, m)->(n, m)')
def cuda_kernel_from_line_13(in_mat, out_mat):
    for i in range(len(in_mat)):
        for j in range(len(out_mat)):
            out_mat[i, j] = math.sin(in_mat[i, j])

    
def main():
    n = 1000
    in_mat = np.random.random((n, n))
    out_mat = np.empty((n, n), np.float64)

    start = time()

    cuda_kernel_from_line_13(in_mat, out_mat)
    end = time()
    print(end - start)


if __name__ == '__main__':
    main()

