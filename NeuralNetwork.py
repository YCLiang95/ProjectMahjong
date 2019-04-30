import ConvolutionalNeuralNetwork
import NeuralNetworkGPU
import FlattenLayer
import pickle
import numpy as np


def uniform_crossover(father, mother):
    result = []
    child_1 = father
    child_2 = mother
    result.append(child_1)
    result.append(child_2)
    return result


class NeuralNetwork:
    fitness = 0
    mutation_rate = 0.2

    def __init__(self):
        self.inputLayer = None
        self.layers = []
        self.outputLayer = None

    def __lt__(self, other):
        return self.fitness < other.fitness

    def add_convolutional_layer(self, shape=(128, 34, 4), filter_shape=(3, 2), height=128, activation="Relu"):
        nn = ConvolutionalNeuralNetwork.ConvolutionalLayer(shape, filter_shape, height)
        self.layers.append(nn)

    def add_flatten_layer(self):
        nn = FlattenLayer.FlattenLayer()
        self.layers.append(nn)

    def add_multilayer_perceptron(self, shape=(34, 128, 128, 34)):
        nn = NeuralNetworkGPU.MLP(shape)
        self.layers.append(nn)

    def evaluate(self):
        for layer in self.layers:
            layer.inputLayer = self.inputLayer
            layer.evaluate()
            self.inputLayer = layer.outputLayer
        self.outputLayer = self.inputLayer

    def mutate(self):
        for layer in self.layers:
            layer.mutate()

    def save(self, filename):
        # use np savez
        with open(filename, 'wb') as file:
            pickle.dump(self.layers, file, pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.layers = pickle.load(file)
