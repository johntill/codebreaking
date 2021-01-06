import timeit

code_to_test = """
import random

key_len = 50

for _ in range(100_000):
    a = list(range(key_len))
    #b = random.sample(a, key_len)
    random.shuffle(a)

#print(a)
#print(b)

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)