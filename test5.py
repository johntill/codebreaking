import time

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
key_len = len(alphabet)
#key = [*alphabet]
#print_key(key)
#print(key)
start = time.perf_counter()
for _ in range(1):
    key1 = [idx for idx in range(key_len)]
    key2 = [*range(key_len)]

print(key1)
print(key2)
end = time.perf_counter()
print(f'{end-start}s')