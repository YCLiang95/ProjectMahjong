import math
import random
import numpy
from numba import cuda, float32


size = 512

@cuda.jit
def matmul(neurons, connections, result):
    sA = cuda.shared.array(shape=(size, size), dtype=float32)
    sB = cuda.shared.array(shape=(size, size), dtype=float32)
    x, y = cuda.grid(2)
    tx = cuda.threadIdx.x
    ty = cuda.threadIdx.y

    if x >= result.shape[0] and y >= result.shape[1]:
        return

        tmp = 0.
        for k in range(A.shape[1]):
            tmp += A[i, k] * B[k, j]
        result[i, j] = tmp


class NeuralNetwork:

    def __init__(self, layers=[34, 255, 255, 34]):
        self.fitness = 0
        self.neurons = []
        for i in layers:
            a = []

        pass

    def __lt__(self, other):
        return self.fitness < other.fitness

    def encode(self):
        pass

    def mutate(self):
        pass

    def reset(self):
        pass

    def evaluate(self):
        pass

    # print the neural network and save it to file
    def save(self, path):
        pass

    # load a neural network from file
    def load(self, path):
        pass
