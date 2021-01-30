from time import perf_counter
import numpy as np
import numpy_indexed as npi
import cipher_tools as tools

start = perf_counter()

cipher_file = 'texts/Code_texts/vigtest2.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = tools.import_cipher(cipher_file)
text_len = len(text)

ngrams = {}
with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
    for line in f:
        ngram, _, count = line.partition(' ')
        ngrams[ngram] = int(count)

names = np.array([[ord(c)-65 for c in key] for key in ngrams])
vals = np.array(list(ngrams.values()), dtype=np.int64)

L = len(ngram)
N = vals.sum()
vals = np.log10(vals / N)
floor = np.log10(0.01 / N)
vals = np.append(vals, floor)
length = vals.size - 1


def new_shape(data, key_len):
    return np.reshape(data, (key_len, -1), order='F')

def add_filler(data, extra_columns):
    temp = np.empty((extra_columns), dtype=int)
    temp.fill(26)
    return np.append(data, temp)

def calculate_IC_2D(text, mod):
    rows, columns = text.shape
    offset = rows * 27
    shifts = np.arange(0, offset, 27)
    text1 = np.add(plain, shifts[:, None]).flat
    results = np.bincount(text1, minlength=offset)
    results1 = np.reshape(results, (rows, -1))
    results2 = results1[:, :-1]
    results3 = np.multiply(results2, results2-1)
    results4 = results3.sum(axis=1)
    N = columns * (columns-1)
    if mod:
        n = np.empty(rows)
        n.fill(N)
        n[mod:] = (columns-1) * (columns-2)
        N = n
    return np.mean(results4 / N)

def strided_app(a, L, S ):  # Window len = L, Stride len/stepsize = S
    nrows = ((a.size-L)//S)+1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a, shape=(nrows,L), strides=(S*n,n))

cipher = np.fromiter(text, dtype='c').view(np.int8) - 65


for poss_len in range(2, 31):
    mod = text_len % poss_len
    if mod:
        plain = add_filler(cipher, poss_len-mod)
        plain = new_shape(plain, poss_len)
    else:
        plain = new_shape(cipher, poss_len)
    IC = calculate_IC_2D(plain, mod)
    if IC > 0.06:
        key_len = poss_len
        break
else:
    print('No viable keylength found.')
    quit()

key = np.zeros((26,1,key_len), dtype=int)

plain1 = plain.swapaxes(0,1)

plain = np.broadcast_to(plain1, (26,)+plain1.shape)

range1 = text_len - L + 1
extra = key_len - mod
range2 = text_len + extra

for _ in range(1):
    for n in range(key_len):
        key[:,0,n] = range(26)

        guess = np.mod(np.subtract(plain, key), 26)

        guess1 = guess.flatten()
        qgrams = strided_app(guess1, 4, 1)

        qg = npi.indices(names, qgrams, missing=length)

        score = np.zeros((26,1))
        for i in range(26):
            range3 = i * range2
            res = qg[0+range3:range1+range3]
            score[i] = vals[res].sum()

        best = np.argmax(score)
        key[:,0,n] = best



key = (key[0] + 65).flat
key = "".join([chr(item) for item in key])

translation = (guess[best] + 65).flat
translation = translation[:-extra]
plain_text = "".join([chr(number) for number in translation])

end = perf_counter()

print(f"Key = {key}")
print(plain_text.lower())

print(f'{end-start}s')
