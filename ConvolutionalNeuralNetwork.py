import numpy as np
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32, xoroshiro128p_normal_float32
from timeit import default_timer as time
import math


@cuda.jit('void(f4[:,:,:], f4[:,:,:], f4[:,:,:,:])')
def apply_filter(input, filter, output):
    x = cuda.blockIdx.x
    y = cuda.blockIdx.y
    i = cuda.threadIdx.x
    j = cuda.threadIdx.y
    # if x < input.shape[0] and y < input.shape[1]:
    if i < output.shape[2] and j < output.shape[3]:
        for a in range(filter.shape[1]):
            for b in range(filter.shape[2]):
                output[x, y, i, j] += input[x, i + a, j + b] * filter[y, a, b]
                # output[x, y, i, j] = 1


@cuda.jit('void(f4[:,:,:,:], f4[:,:,:], int32)')
def sum_up(input, output, input_height):
    x = cuda.blockIdx.x
    i = cuda.threadIdx.x
    j = cuda.threadIdx.y
    for a in range(input_height):
        output[x, i, j] += input[a, x, i, j]
    output[x, i, j] = max(0, output[x, i, j])


@cuda.jit
def mutate_gpu(filter, rate, rng_states):
    thread_id = cuda.grid(1)
    if thread_id == 0:
        cuda.syncthreads()
    a = xoroshiro128p_uniform_float32(rng_states, thread_id)
    if a < rate:
        x = cuda.blockIdx.x
        i = cuda.threadIdx.x
        j = cuda.threadIdx.y
        b = xoroshiro128p_uniform_float32(rng_states, thread_id) * 2 - 1
        filter[x, i, j] += b


class ConvolutionalLayer:
    mutation_rate = 0.2

    def __init__(self, shape=(128, 34, 4), filter_shape=(3, 2), height=128, activation="Relu"):
        self.height = height
        self.shape = shape
        self.filter_shape = filter_shape
        self.activation = activation
        self.inputLayer = np.zeros(shape=shape, dtype=np.float32)
        self.outputLayer = np.zeros(shape=(height, shape[1] - filter_shape[0] + 1, shape[2] - filter_shape[1] + 1), dtype=np.float32)
        self.filter = np.array(np.random.uniform(low=-1.0, high=1.0, size=(height, filter_shape[0], filter_shape[1])), dtype=np.float32)
        # self.rng_states = create_xoroshiro128p_states(self.height * self.filter_shape[0] * self.filter_shape[1], seed=1)

    def mutate_gpu(self):
        dA = cuda.to_device(self.filter)
        mutate_gpu[self.height, (self.filter_shape[0], self.filter_shape[1])](dA, self.mutation_rate, self.rng_states)
        dA.to_host()

    def mutate(self):
        for i in range(self.height):
            for j in range(self.filter_shape[0]):
                for k in range(self.filter_shape[1]):
                    q = np.random.uniform(low=0.0, high=1.0, size=1)
                    if q < 0.2:
                        self.filter[i, j, k] += np.random.uniform(low=-1.0, high=1.0, size=1)

    def evaluate(self):
        temp = np.zeros(shape=(self.shape[0], self.height, self.shape[1] - self.filter_shape[0] + 1,
                               self.shape[2] - self.filter_shape[1] + 1), dtype=np.float32)
        self.outputLayer = np.zeros(shape=(self.height, self.shape[1] - self.filter_shape[0] + 1,
                                           self.shape[2] - self.filter_shape[1] + 1), dtype=np.float32)
        dA = cuda.to_device(self.inputLayer)
        dB = cuda.to_device(self.filter)
        dC = cuda.to_device(temp)
        dD = cuda.to_device(self.outputLayer)
        apply_filter[(self.shape[0], self.height), (self.shape[1], self.shape[2])](dA, dB, dC)
        sum_up[self.height, (self.shape[1] - self.filter_shape[0] + 1,
                             self.shape[2] - self.filter_shape[1] + 1)](dC, dD, self.shape[0])
        dD.to_host()

    def evaluate_cpu(self):
        self.outputLayer = np.zeros(shape=(self.height, self.shape[1] - self.filter_shape[0] + 1,
                                           self.shape[2] - self.filter_shape[1] + 1))
        for i in range(self.height):
            for j in range(self.shape[0]):
                for k in range(self.shape[1] - self.filter_shape[0] + 1):
                    for l in range(self.shape[2] - self.filter_shape[1] + 1):
                        for a in range(self.filter_shape[0]):
                            for b in range(self.filter_shape[1]):
                                self.outputLayer[i][k][l] += self.inputLayer[j][k + a][l + b] * self.filter[i][a][b]
        for i in range(self.height):
            for j in range(len(self.outputLayer[0])):
                for k in range(len(self.outputLayer[0][0])):
                    if self.activation == "Relu":
                        self.outputLayer[i][j][k] = max(0, self.outputLayer[i][j][k])
