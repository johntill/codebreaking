from time import perf_counter
import numpy as np

ngram_file = 'texts/Frequencies/english_quadgrams.txt'

def gen_dict1(ngram_file):
    ngrams = {}
    with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
        for line in f:
            key, _, count = line.partition(' ')
            ngrams[key] = int(count)

    names = np.array([[ord(c)-65 for c in key] for key in ngrams])
    vals = np.array(list(ngrams.values()), dtype=np.int64)

    L = len(key)
    N = vals.sum()
    vals = np.log10(vals / N)
    #floor = np.log10(0.01 / N)
    #vals = np.append(vals, floor)
    length = vals.size
    return names, vals, L, length

def gen_dict2(ngram_file):
    names = []
    vals = []
    with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
        for line in f:
            key, _, count = line.partition(' ')
            names.append([ord(c)-65 for c in key])
            vals.append(int(count))

    names = np.array(names)
    vals = np.array(vals, dtype=np.float64)

    L = len(key)
    N = vals.sum()
    vals = np.log10(vals / N)
    floor = np.log10(0.01 / N)
    vals = np.append(vals, floor)
    length = vals.size - 1
    return names, vals, L, length

def gen_dict3(ngram_file):
    ngrams = {}
    with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
        for line in f:
            key, _, count = line.partition(' ')
            ngrams[key] = int(count)

    names = np.array([[ord(c)-65 for c in key] for key in ngrams])
    vals = np.array(list(ngrams.values()), dtype=np.int64)

    L = len(key)
    N = vals.sum()
    vals = np.log10(vals / N)
    floor = np.log10(0.01 / N)
    vals = np.append(vals, floor)
    length = vals.size - 1
    return names, vals, L, length


start = perf_counter()
for _ in range(1):
    names, vals, L, length = gen_dict1(ngram_file)
    #names, vals, L, length = gen_dict2(ngram_file)
    #names, vals, L, length = gen_dict3(ngram_file)

end = perf_counter()

# print(names)
# print(names.dtype)
# print(vals)
# print(vals.dtype)


print(f'{end-start}s')