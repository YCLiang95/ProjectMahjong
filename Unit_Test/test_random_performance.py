import time
import random
import numpy as np

t = time.time()
for i in range(1000000):
    a = random.random()
print(round(time.time() - t))

t = time.time()
for i in range(1000000):
    a = np.random.uniform(-1.0, 1.0)
print(round(time.time() - t))
