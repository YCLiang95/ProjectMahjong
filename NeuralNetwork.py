import ConvolutionalNeuralNetwork
import NeuralNetworkGPU

class NeuralNetwork:
    fitness = 0
    mutation_rate = 0.2

    def __init__(self):
        self.inputLayer = []
        self.layers = []
        self.outputLayer = []

    def add_convolutional_layer(self, shape=(128, 34, 4), filter_shape=(3, 2), height=128, activation="Relu"):
        pass

    def add_multilayer_perceptron(self):
        pass

    def evaluate(self):
        for layer in self.layers:
            layer.inputLayer = self.inputLayer
            layer.evaluate()
            self.inputLayer = layer.outputLayer
        self.outputLayer = self.inputLayer

    def mutate(self):
        for layer in self.layers:
            layer.mutate()
