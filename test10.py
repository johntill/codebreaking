from time import perf_counter
import numpy as np

a = np.arange(200)

start = perf_counter()
for _ in range(2_000_000):
    #a = a.reshape((10,-1))
    b = a.reshape((10,-1))
    
print(b.base)



end = perf_counter()

print(f'{end-start}s')