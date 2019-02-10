import math
import base64


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def breed(father, mother):
    pass


class Neuron:
    value = 0
    activation = sigmoid
    connections = []
    layer = 0
    active = False

    def __init__(self, layer, next_layer):
        self.layer = layer
        for i in range(next_layer):
            self.connections.append(0.0)
        self.value = 0

    def activate(self):
        self.value = self.activation(self.value)


class NeuralNetwork:
    geno = ""
    depth = 2
    layers = []
    NeuronCounts = []

    def __init__(self, layers=[255, 255, 255, 255]):
        self.NeuronCounts = layers
        self.depth = len(layers) - 2
        for i in range(len(layers)):
            self.layers.append([])
            for j in range(layers[i]):
                if i == len(layers) - 1:
                    self.layers[i + 1].append(Neuron(i + 1, 0))
                else:
                    self.layers[i + 1].append(Neuron(i + 1, layers[i + 1]))

    def random_generator(self):
        for i in range(10):
            pass
        self.encode()

    def encode(self):
        geno = ""
        geno = geno + "F" + str(len(self.layers[1])) + "S" + str(len(self.layers[2]))
        self.geno = base64.encodebytes(bytes(geno, encoding="ascii"))

    def mutate(self):
        self.encode()

    def reset(self):
        for i in range(1, len(self.layers)):
            for j in self.layers[i]:
                j.value = 0
                j.active = False

    def evaluate(self):
        self.reset()
        for i in range(self.depth + 1):
            for j in self.layers[i]:
                if j.active or i == 0:
                    for k in range(len(j.connections)):
                        self.layers[i + 1][k].value += j.value * j.connections[k]
                        self.layers[i + 1][k].active = True
            for j in self.layers[i + 1]:
                if j.active:
                    j.activate()
