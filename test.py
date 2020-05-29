import itertools
import random

# swap any 2 elements
# swap any 2 columns
# swap any 2 rows
# permutations of all 5 rows
# permutations of all 5 columns
# permutations of all 5 elements in a row
# permutations of all 5 elements in a column

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

def swap_row(key):
    iter2 = itertools.permutations(range(0,25,5),2)
    for x, y in iter2:
        key[y:y+5], key[x:x+5] = key[x:x+5], key[y:y+5]
        yield key

def swap_column(key):
    iter3 = itertools.permutations(range(5),2)
    for x, y in iter3:
        key[y::5], key[x::5] = key[x::5], key[y::5]
        yield key

def score_key(key):
    return 1

#score = (score_key(key) for key in swap_element(key))
for key in swap_element(key):
    count += score_key(key)

for key in swap_row(key):
    count += score_key(key)

for key in swap_column(key):
    count += score_key(key)

print(count)
key = ''.join(key)
for i in range(0, 25, 5):
    print(key[i:i+5])

count2 = 0
iter4 = itertools.permutations('ABCD', 4)
for i in iter4:
    count2 += 1
    print(i)

print(count2)
