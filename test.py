import itertools
import random

# swap any 2 elements
# swap any 2 columns
# swap any 2 rows
# permutations of all 5 rows
# permutations of all 5 columns
# permutations of all 5 elements in a row
# permutations of all 5 elements in a column

def swap_all_elements(key):
    perms = itertools.combinations(range(25),2)
    for x, y in perms:
        key[x], key[y] = key[y], key[x]
        yield key

def swap_all_rows(key):
    perms = itertools.permutations(range(0,25,5),5)
    new_key = [None] * 25
    for perm in perms:
        for i in range(5):
            new_key[i*5:i*5+5] = key[perm[i]:perm[i]+5]
        yield new_key

def swap_all_columns(key):
    perms = itertools.permutations(range(5),5)
    new_key = [None] * 25
    for perm in perms:
        for i in range(5):
            new_key[i::5] = key[perm[i]::5]
        yield new_key

def swap_row_elements(key):
    for i in range(0,25,5):
        new_key = [*key]
        perms = itertools.permutations(range(5),5)
        for perm in perms:
            for j in range(5):
                new_key[i+j] = key[i+perm[j]]
            yield new_key

def swap_column_elements(key):
    for i in range(5):
        new_key = [*key]
        perms = itertools.permutations(range(0,25,5),5)       
        for perm in perms:
            for j in range(5):
                new_key[i+j*5] = key[i+perm[j]]
            yield new_key

def score_key(key):
    return 1

def print_key(key):
    show_key = ''.join(key)
    for i in range(0, 25, 5):
        print(show_key[i:i+5])

alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

#key = random.sample(alphabet, 25)
key = list(alphabet)

print_key(key)
count = 0

#score = (score_key(key) for key in swap_element(key))

options = ([swap_all_elements, swap_all_rows, swap_all_columns,
            swap_row_elements, swap_column_elements])

for option in options:
    for key in option(key):
        count += score_key(key)
    print_key(key)

# for key in swap_column_elements(key):
#     count += score_key(key)
# print_key(key)


print(count)
