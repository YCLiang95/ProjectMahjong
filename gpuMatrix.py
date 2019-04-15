from numba import cuda
import numpy as np
import math
from timeit import default_timer as time

BLOCK_SIZE = 100


@cuda.jit('void(f4[:], f4[:], int32)')
def sigmoid_activate(vector, result, m):
    index = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    if index < m:
        result[index] = 1.0 / (1.0 + math.exp(-vector[index]))


@cuda.jit('void(f4[:,:], f4[:], f4[:], int32, int32)')
def cu_matrix_vector(matrix, vector, result, m, n):
    row = cuda.grid(1)
    if row < m:
        temp = 0
        for i in range(n):
            temp += matrix[row, i] * vector[row]
        result[row] = temp


m = 100000
n = 100

A = np.array(np.random.uniform(low=-1.0, high=1.0, size=(m, n)), dtype=np.float32)
B = np.array(np.random.random(m), dtype=np.float32)
C = np.empty_like(B)
D = np.empty_like(B)

s = time()
dA = cuda.to_device(A)
dB = cuda.to_device(B)
dC = cuda.to_device(C)
# dD = cuda.to_device(D)

cu_matrix_vector[(m+511)//512, 512](dA, dB, dC, m, n)
# sigmoid_activate[(m+511)//512, 512](dC, dD)

dC.to_host()
# dD.to_host()

print(C)
# print(D)

e = time()
tcuda = e - s

print(tcuda)

C = np.zeros_like(B)
D = np.empty_like(B)

s = time()
for i in range(m):
    for j in range(n):
        C[i] += A[i, j] * B[i]
#for i in range(m):
#    D[i] = 1.0 / (1.0 + math.exp(-C[i]))

print(C)
#print(D)

e = time()
tcuda = e - s
print(tcuda)