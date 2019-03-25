import math
import random
import base64
import json

def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def create(layers):
    return NeuralNetwork(layers)


def load(file):
    nn = NeuralNetwork()
    nn.__dict__ = json.load(file)
    return nn


def save(nn, file):
    json.dump(nn.__dict__, file)


# crossover 2 neural network with an random point
# return: produce 2 offsprings
def point_crossover(father, mother):
    result = []
    child1 = NeuralNetwork(father.NeuronCounts)
    child2 = NeuralNetwork(mother.NeuronCounts)
    point = random.randint(0, father.count)
    for i in range(point):
        pass
    for i in range(point, father.count):
        pass
    result.append(child1)
    result.append(child2)
    return result


# uniformly crossover two neural network with each weight
# return: produce 2 offsprings
def uniform_crossover(father, mother):
    result = []
    child1 = NeuralNetwork(father.NeuronCounts)
    child2 = NeuralNetwork(mother.NeuronCounts)
    for i in range(len(father.layers) - 1):
        for j in range(len(father.layers[i])):
            if random.randint(0, 1) == 1:
                child1.layers[i][j].clone(father.layers[i][j])
                child2.layers[i][j].clone(mother.layers[i][j])
            else:
                child2.layers[i][j].clone(father.layers[i][j])
                child1.layers[i][j].clone(mother.layers[i][j])
    if random.randint(0, 100) >= 25:
        child1.mutate()
    if random.randint(0, 100) >= 25:
        child2.mutate()
    result.append(child1)
    result.append(child2)
    return result


# Neural network class, core of neural network
class Neuron:
    # activation = sigmoid

    def __init__(self, layer, next_layer):
        self.layer = layer
        self.active = False
        self.value = 0
        self.connections = []
        for i in range(next_layer):
            #self.connections.append(random.random() * 2 - 1)
            self.connections.append(0.0)
        self.value = 0

    def activate(self):
        # self.value = self.activation(self.value)
        self.value = sigmoid(self.value)

    def clone(self, parent):
        self.layer = parent.layer
        self.connections = parent.connections.copy()


class NeuralNetwork:

    def __init__(self, layers=[34, 255, 255, 34]):
        self.NeuronCounts = layers
        self.counts = 0
        self.fitness = 0.0
        self.mutationCount = 25
        self.geno = ""
        for i in range(1, len(layers) - 1):
            self.counts += layers[i]
        self.depth = len(layers) - 2
        self.layers = []
        for i in range(len(layers)):
            self.layers.append([])
            for j in range(layers[i]):
                if i == len(layers) - 1:
                    self.layers[i].append(Neuron(i, 0))
                else:
                    self.layers[i].append(Neuron(i, layers[i + 1]))

    def __lt__(self, other):
        return self.fitness < other.fitness

    def random_generator(self):
        for i in range(10):
            pass
        self.encode()

    def encode(self):
        geno = ""
        geno = geno + "F" + str(len(self.layers[1])) + "S" + str(len(self.layers[2]))
        self.geno = base64.encodebytes(bytes(geno, encoding="ascii"))

    # make sure all connected middle neuron has a path to next node
    def validate(self):
        pass

    def mutate(self):
        for i in range(random.randint(1, self.mutationCount)):
            j = random.randint(0, len(self.layers) - 2)
            k = random.randint(0, self.NeuronCounts[j] - 1)
            m = random.randint(0, self.NeuronCounts[j + 1] - 1)
            if random.randint(0, 100) >= 5:
                self.layers[j][k].connections[m] += random.random() * 4 - 2
            else:
                self.layers[j][k].connections[m] = 0
        self.validate()
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
                        if j.connections[k] != 0:
                            self.layers[i + 1][k].value += j.value * j.connections[k]
                            self.layers[i + 1][k].active = True
            for j in self.layers[i + 1]:
                if j.active:
                    j.activate()

    # print the neural network and save it to file
    def save(self, path):
        with open(path, 'w+') as file:
            file.write(str(len(self.layers)) + '\n')
            for i in range(len(self.layers)):
                file.write(str(len(self.layers[i])) + '\n')
            for i in range(self.depth + 1):
                for j in self.layers[i]:
                    for k in j.connections:
                        file.write(str(round(k, 3)) + '\n')
        file.close()

    # load a neural network from file
    def load(self, path):
        with open(path, 'r') as file:
            self.depth = int(file.readline())
            self.NeuronCounts = []
            for i in range(self.depth):
                self.NeuronCounts.append(int(file.readline()))
            self.layers = []
            for i in range(len(self.NeuronCounts)):
                self.layers.append([])
                for j in range(self.NeuronCounts[i]):
                    if i == len(self.NeuronCounts) - 1:
                        self.layers[i].append(Neuron(i, 0))
                    else:
                        self.layers[i].append(Neuron(i, self.NeuronCounts[i + 1]))
                    for k in range(len(self.layers[i][j].connections)):
                        self.layers[i][j].connections[k] = float(file.readline())
