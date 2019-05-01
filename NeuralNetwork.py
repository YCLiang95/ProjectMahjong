import ConvolutionalNeuralNetwork
import NeuralNetworkGPU
import FlattenLayer
import pickle
import numpy as np


class NeuralNetwork:
    fitness = 0
    mutation_rate = 0.25
    crossover_rate = 0.25

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

    def uniform_crossover(self, network):
        result = []
        child_1 = NeuralNetwork()
        child_2 = NeuralNetwork()
        for i in range(len(self.layers)):
            t = self.layers[i].uniform_crossover(network.layers[i], self.crossover_rate)
            child_1.layers.append(t[0])
            child_2.layers.append(t[1])
        result.append(child_1)
        result.append(child_2)
        return result

    def save(self, filename):
        # use np savez
        with open(filename, 'wb') as file:
            pickle.dump(self.layers, file, pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.layers = pickle.load(file)
