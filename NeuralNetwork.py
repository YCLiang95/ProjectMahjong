import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Edge:
    weight = 0.0
    start = None
    end = None
    layer = 0

    def __init__(self):
        self.weight = 0.0


class Neuron:
    value = 0
    activation = sigmoid

    def __init__(self):
        self.value = 0

    def activate(self):
        return self.activation(self.value)


class NeuralNetwork:
    id = ""
    inputLayer = []
    hiddenLayer1 = []
    hiddenLayer2 = []
    outputLayer = []
    edgesIF = []
    edgesFS = []
    edgesSO = []

    def __init__(self, input_count, output_count):
        for i in range(input_count):
            self.inputLayer.append(Neuron())
        for i in range(output_count):
            self.outputLayer.append(Neuron())
        self.id = "foo"

    def random(self):
        for i in range(10):
            self.inputLayer.append(Neuron())
            print("do something")
            # do something

    def load(self):
        # load items
        return self
