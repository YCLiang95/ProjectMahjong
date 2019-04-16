import numpy as np
from ConvolutionalNeuralNetwork import  ConvolutionalLayer
from timeit import default_timer as time

t = ConvolutionalLayer()
a = np.array(np.random.uniform(low=-1.0, high=1.0, size=(128, 34, 4)), dtype=np.float32)
t.inputLayer = a

tt = time()
t.evaluate()
print(time() - tt)
b = t.outputLayer

tt = time()
t.evaluate_cpu()
print(time() - tt)

d = np.zeros_like(t.outputLayer)

sum = 0.0

for i in range(len(t.outputLayer)):
    for j in range(len(t.outputLayer[0])):
        for k in range(len(t.outputLayer[0][0])):
            d[i][j][k] = abs(b[i][j][k] - t.outputLayer[i][j][k])
            sum += d[i][j][k]

print(d)
print(round(sum / (b.shape[0] * b.shape[1] * b.shape[2]), 5))