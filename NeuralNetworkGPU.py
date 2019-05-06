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


@cuda.jit('void(f4[:,:], f4[:], f4[:], f4[:], int32, int32)')
def sigmoid_layer(matrix, vector, bias, result, m, n):
    row = cuda.grid(1)
    if row < n:
        temp = 0
        for i in range(m):
            temp += matrix[i, row] * vector[i]
        # result[row] = 1.0 / (1.0 + math.exp(-temp - bias[row]))
        # result[row] = math.tanh(temp + bias[row])
        result[row] = temp + bias[row]


@cuda.jit('void(f4[:,:], f4[:], f4[:], f4[:], int32, int32)')
def relu_layer(matrix, vector, bias, result, m, n):
    row = cuda.grid(1)
    if row < n:
        temp = 0
        for i in range(m):
            temp += matrix[i, row] * vector[i]
        result[row] = max(0.0, temp + bias[row])


class MLP:

    def __init__(self, layers=(34, 255, 255, 34)):
        self.fitness = 0
        self.layers = layers
        self.depth = len(layers)
        self.inputLayer = np.zeros(layers[0], dtype=np.float32)
        self.outputLayer = np.zeros(layers[len(layers) - 1], dtype=np.float32)
        self.mutation_rate = 0.2
        self.connection = []
        self.bias = []
        for i in range(len(layers) - 1):
            a = np.array(np.random.uniform(low=-1.0, high=1.0, size=(layers[i], layers[i + 1])), dtype=np.float32)
            self.connection.append(a)
        for i in range(len(layers)):
            a = np.array(np.random.uniform(low=-1.0, high=1.0, size=layers[i]), dtype=np.float32)
            self.bias.append(a)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def mutate(self):
        for i in range(len(self.connection)):
            for j in range(len(self.connection[i])):
                if random.random() < self.mutation_rate:
                    self.connection[i][j] += random.random() * 4 - 2
                    if self.connection[i][j] > 3:
                        self.connection[i][j] = 3
                    elif self.connection[i][j] < -3:
                        self.connection[i][j] = -3
            # self.connection[i].clip(-3.0, 3.0, out=self.connection[i])
        for i in range(1, len(self.bias)):
            for j in range(len(self.bias[i])):
                if random.random() < self.mutation_rate:
                    self.bias[i][j] += random.random() * 4 - 2
                    if self.bias[i][j] > 3:
                        self.bias[i][j] = 3
                    elif self.bias[i][j] < -3:
                        self.bias[i][j] = -3
            # self.bias[i].clip(-1.0, 1.0, out=self.bias[i])

    def uniform_crossover(self, mate, rate):
        result = [MLP(self.layers), MLP(self.layers)]
        for i in range(len(self.layers) - 1):
            for j in range(self.layers[i + 1]):
                for k in range(self.layers[i]):
                    if random.random() > rate:
                        result[0].connection[i][k][j] = self.connection[i][k][j]
                        result[1].connection[i][k][j] = mate.connection[i][k][j]
                    else:
                        result[1].connection[i][k][j] = self.connection[i][k][j]
                        result[0].connection[i][k][j] = mate.connection[i][k][j]
                if random.random() > rate:
                    result[0].bias[i + 1][j] = self.bias[i + 1][j]
                    result[1].bias[i + 1][j] = mate.bias[i + 1][j]
                else:
                    result[1].bias[i + 1][j] = self.bias[i + 1][j]
                    result[0].bias[i + 1][j] = mate.bias[i + 1][j]
        return result

    def evaluate(self):
        layer = self.inputLayer
        for i in range(len(self.layers) - 1):
            output_layer = np.zeros(self.layers[i + 1], dtype=np.float32)
            dA = cuda.to_device(self.connection[i])
            dB = cuda.to_device(layer)
            dC = cuda.to_device(output_layer)
            dD = cuda.to_device(self.bias[i + 1])
            if i == self.depth - 2:
                sigmoid_layer[(self.layers[i + 1] + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE](dA, dB, dD, dC, self.layers[i], self.layers[i + 1])
            else:
                relu_layer[(self.layers[i + 1] + BLOCK_SIZE - 1) // BLOCK_SIZE, BLOCK_SIZE](dA, dB, dD, dC, self.layers[i], self.layers[i + 1])
            dC.to_host()
            layer = output_layer
        self.outputLayer = layer

    def evaluate_cpu(self):
        layer = self.inputLayer
        for i in range(len(self.layers) - 1):
            output_layer = np.zeros(self.layers[i + 1])
            for j in range(self.layers[i]):
                for k in range(self.layers[i + 1]):
                    output_layer[k] += layer[j] * self.connection[i][j][k]

            for k in range(self.layers[i + 1]):
                if i == self.depth - 2:
                    # output_layer[k] = 1.0 / (1.0 + math.exp(-output_layer[k] - self.bias[i + 1][k]))
                    output_layer[k] = output_layer[k] + self.bias[i + 1][k]
                else:
                    output_layer[k] = max(0, output_layer[k] + self.bias[i + 1][k])

            layer = output_layer
        self.outputLayer = layer

    def encode(self):
        pass

    # print the neural network and save it to file
    def save(self, path):
        pass

    # load a neural network from file
    def load(self, path):
        pass
