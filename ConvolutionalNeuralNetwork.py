import numpy as np


class ConvolutionalLayer:
    def __init__(self, shape=(128, 34, 4), filter_shape=(3, 2), height=128, activation="Relu"):
        self.height = height
        self.shape = shape
        self.filter_shape = filter_shape
        self.activation = activation
        self.inputLayer = np.zeros(shape=shape)
        self.outputLayer = np.zeros(shape=(height, shape[1] - filter_shape[0] + 1, shape[2] - filter_shape[1] + 1))
        self.filter = np.array(np.random.uniform(low=-1.0, high=1.0, size=(height, filter_shape[0], filter_shape[1])))

    def evaluate_cpu(self):
        self.outputLayer = np.zeros(shape=(self.height, self.shape[1] - self.filter_shape[0] + 1,
                                           self.shape[2] - self.filter_shape[1] + 1))
        for i in range(self.height):
            for j in range(self.shape[0]):
                for k in range(self.shape[1] - self.filter_shape[0] + 1):
                    for l in range(self.shape[2] - self.filter_shape[1] + 1):
                        for a in range(self.filter_shape[0]):
                            for b in range(self.filter_shape[1]):
                                self.outputLayer[i][k][l] += self.inputLayer[j][k + a][l + b] * self.filter[i][a][b]
        for i in range(self.height):
            for j in range(len(self.outputLayer[0])):
                for k in range(len(self.outputLayer[0][0])):
                    if self.activation == "Relu":
                        self.outputLayer[i][j][k] = max(0, self.outputLayer[i][j][k])


t = ConvolutionalLayer()
a = np.array(np.random.uniform(low=-1.0, high=1.0, size=(128, 34, 4)), dtype=np.float32)
t.inputLayer = a
t.evaluate_cpu()
print(t.outputLayer)
