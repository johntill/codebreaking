import itertools
import random

alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

#key = random.sample(alphabet, 25)
key = list(alphabet)

print(key)
count = 0

def swap_element(key):
    iter1 = itertools.combinations(range(25),2)
    for x, y in iter1:
        key[x], key[y] = key[y], key[x]
        yield key

def score_key(key):
    pass

#score = (score_key(key) for key in swap_element(key))
for key in swap_element(key):
    score = score_key(key)
    count += 1


print(count)