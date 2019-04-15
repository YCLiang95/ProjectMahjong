import numpy as np
from numba import cuda
import NeuralNetworkGPU
from timeit import default_timer as time

NN = NeuralNetworkGPU.NeuralNetwork()
input = np.array(np.random.uniform(low=-1.0, high=1.0, size=34), dtype=np.float32)
NN.inputLayer = input
t = time()
NN.evaluate()
output1 = NN.outputLayer
print(t - time())

t = time()
NN.evaluate_cpu()
output2 = NN.outputLayer
print(t - time())

print("Error")
for i in range(len(output1)):
    print(abs(output1[i] - output2[i]))