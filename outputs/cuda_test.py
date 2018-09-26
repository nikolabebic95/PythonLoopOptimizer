import numba
import numpy as np
import math
from time import time


# WARNING!!!
# If the actual types are not all float64, you must edit the corresponding  value in the 'guvectorize' decorator.
# The order of the types in the decorator is the same as the order of the function parameters
# This function also assumes the shape of the output array
# If the shape is not correct, it must be corrected by the user
@numba.guvectorize([(numba.float64[:, :], numba.float64[:, :])], '(a, b)->(a, b)')
def cuda_kernel_from_line_13(in_mat, out_mat):
    for i in range(in_mat.shape[0]):
        for j in range(in_mat.shape[1]):
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

