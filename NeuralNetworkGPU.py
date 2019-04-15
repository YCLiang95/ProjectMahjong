import math
import random
import numpy as np
from numba import cuda

m = 512
n = 512
BLOCK_SIZE = 512


@cuda.jit('void(f4[:], f4[:])')
def sigmoid_activate(vector):
    index = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    if index < m:
        vector[index] = 1.0 / (1.0 + math.exp(-vector[index]))


@cuda.jit('void(f4[:,:], f4[:], f4[:])')
def sigmoid_layer(matrix, vector, result):
    row = cuda.grid(1)
    if row < m:
        temp = 0
        for i in range(n):
            temp += matrix[row, i] * vector[row]
        result[row] = 1.0 / (1.0 + math.exp(-vector[temp]))


@cuda.jit('void(f4[:,:], f4[:], f4[:])')
def relu_layer(matrix, vector, result):
    row = cuda.grid(1)
    if row < m:
        temp = 0
        for i in range(n):
            temp += matrix[row, i] * vector[row]
        result[row] = max(0.0, temp)


class NeuralNetwork:
    def __init__(self, layers=[34, 255, 255, 34]):
        self.fitness = 0
        self.layers = layers
        self.depth = len(layers)
        self.inputLayer = np.zeros(layers[0])
        self.outputLayer = np.zeros(layers[len(layers) - 1])
        self.connection = []
        for i in range(len(layers) - 1):
            a = np.array(np.random.uniform(low=-1.0, high=1.0, size=(layers[i], layers[i + 1])), dtype=np.float32)
            self.connection.append(a)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def encode(self):
        pass

    def mutate(self):
        pass

    def reset(self):
        pass

    def evaluate(self):
        layer = self.inputLayer
        for i in range(len(self.layers) - 1):
            output_layer = np.zeros(self.layers[i + 1])
            dA = cuda.to_device(layer)
            dB = cuda.to_device(self.connection[i])
            dC = cuda.to_device(output_layer)
            if i == self.depth - 2:
                sigmoid_layer[(self.layers[i] + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE](dA, dB, dC)
            else:
                relu_layer[(self.layers[i] + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE](dA, dB, dC)
            dC.copy_to_host()
            layer = output_layer
        self.outputLayer = layer

    # print the neural network and save it to file
    def save(self, path):
        pass

    # load a neural network from file
    def load(self, path):
        pass
