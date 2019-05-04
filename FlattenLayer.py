class FlattenLayer:

    def __init__(self):
        self.inputLayer = None
        self.outputLayer = None

    def mutate(self):
        pass

    def evaluate(self):
        self.outputLayer = self.inputLayer.flatten()

    def uniform_crossover(self, mate, rate):
        result = [self, mate]
        return result

    def evaluate_cpu(self):
        self.evaluate()

    def encode(self):
        pass

    # print the neural network and save it to file
    def save(self, path):
        pass

    # load a neural network from file
    def load(self, path):
        pass
