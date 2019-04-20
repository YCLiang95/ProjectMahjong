import ConvolutionalNeuralNetwork
import NeuralNetworkGPU


def uniform_crossover(father, mother):
    result = []
    result.append(father)
    result.append(mother)
    return result


class NeuralNetwork:
    fitness = 0
    mutation_rate = 0.2

    def __init__(self):
        self.inputLayer = []
        self.layers = []
        self.outputLayer = []

    def add_convolutional_layer(self, shape=(128, 34, 4), filter_shape=(3, 2), height=128, activation="Relu"):
        nn = ConvolutionalNeuralNetwork.ConvolutionalLayer(shape, filter_shape, height)
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
        pass

    def load(self, filename):
        pass
