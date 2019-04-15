import math
import random
import numpy as np
from numba import cuda

BLOCK_SIZE = 512


@cuda.jit('void(f4[:], int32)')
def sigmoid_activate(vector, m):
    index = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    if index < m:
        vector[index] = 1.0 / (1.0 + math.exp(-vector[index]))


@cuda.jit('void(f4[:,:], f4[:], f4[:], int32, int32)')
def sigmoid_layer(matrix, vector, result, m, n):
    row = cuda.grid(1)
    if row < n:
        temp = 0
        for i in range(m):
            temp += matrix[i, row] * vector[i]
        result[row] = 1.0 / (1.0 + math.exp(-temp))


@cuda.jit('void(f4[:,:], f4[:], f4[:], int32, int32)')
def relu_layer(matrix, vector, result, m, n):
    row = cuda.grid(1)
    if row < n:
        temp = 0
        for i in range(m):
            temp += matrix[i, row] * vector[i]
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
                sigmoid_layer[(self.layers[i + 1] + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE](dA, dB, dC, self.layers[i], self.layers[i + 1])
            else:
                relu_layer[(self.layers[i + 1] + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE](dA, dB, dC, self.layers[i], self.layers[i + 1])
            dC.copy_to_host()
            layer = output_layer
        self.outputLayer = layer

    def evaluate_cpu(self):
        layer = self.inputLayer
        for i in range(len(self.layers) - 1):
            output_layer = np.zeros(self.layers[i + 1])
            for j in range(self.layers[i]):
                for k in range(self.layers[i + 1]):
                    output_layer[k] += layer[j] * self.connection[j][k]

            for k in range(self.layers[i + 1]):
                if i == self.depth - 2:
                    output_layer[k] = 1.0 / (1.0 + math.exp(-output_layer[k]))
                else:
                    output_layer[k] = max(0, output_layer[k])

            layer = output_layer
        self.outputLayer = layer

    # print the neural network and save it to file
    def save(self, path):
        pass

    # load a neural network from file
    def load(self, path):
        pass
