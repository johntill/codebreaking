import time

alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" 

start = time.perf_counter()

for _ in range(1_000_000):
    alphabet_sequence = [*range(len(alphabet))]
    #alphabet_sequence = list(range(len(alphabet)))

#print(alphabet_sequence)

end = time.perf_counter()
print(f'{end-start}s')
