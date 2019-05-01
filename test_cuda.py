import numpy as np
from numba import cuda
import NeuralNetworkGPU
from timeit import default_timer as time

NN = NeuralNetworkGPU.MLP()
input = np.array(np.random.uniform(low=0, high=1.0, size=34), dtype=np.float32)
NN.inputLayer = input
t = time()
NN.evaluate()
output1 = NN.outputLayer
print(time() - t)

t = time()
NN.evaluate_cpu()
output2 = NN.outputLayer
print(time() - t)

print(output1)

print(output2)

NN.mutate()

t = time()
NN.evaluate()
output1 = NN.outputLayer
print(time() - t)

t = time()
NN.evaluate_cpu()
output2 = NN.outputLayer
print(time() - t)

print(output1)

print(output2)
