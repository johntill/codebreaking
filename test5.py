import time
import itertools
import random

def swap_4_letter_groups(key):
    for s in range(len(key)-7):
        s1 = key[s:s+4]
        for p in range(s+4,len(key)-3):
            new_key = [*key]
            p1 = key[p:p+4]
            new_key[s:s+4], new_key[p:p+4] = p1, s1
            yield new_key


def print_key(key):
    show_key = ''.join(key)
    for i in range(0, 25, 5):
        print(show_key[i:i+5])
    print()

alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
key = list(alphabet)
#print_key(key)
#print(key)
start = time.perf_counter()
count = 0
for new_key in swap_4_letter_groups(key):
    #print_key(new_key)
    count += 1
    #print(new_key)

#new_key = TR_BL_mirror(key)
#print(count)
#print_key(new_key)

end = time.perf_counter()
print(f'{end-start}s')