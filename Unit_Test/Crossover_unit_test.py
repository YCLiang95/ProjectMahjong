import NeuralNetwork
from timeit import default_timer as time

a1 = NeuralNetwork.NeuralNetwork()
a2 = NeuralNetwork.NeuralNetwork()
a1.add_convolutional_layer(shape=(6, 34, 4))
a1.add_convolutional_layer(shape=(6, 32, 3))
a1.add_convolutional_layer(shape=(6, 30, 2))
a1.add_flatten_layer()
a1.add_multilayer_perceptron(shape=(360, 255, 128, 34))

a2.add_convolutional_layer(shape=(6, 34, 4))
a2.add_convolutional_layer(shape=(6, 32, 3))
a2.add_convolutional_layer(shape=(6, 30, 2))
a2.add_flatten_layer()
a2.add_multilayer_perceptron(shape=(360, 255, 128, 34))

t = time()
result = a1.uniform_crossover(a2)
print(time() - t)
