from time import perf_counter
import numpy as np
import numpy_indexed as npi


text = 'nmskxlgnomnydenrvwszrmpgcbyk'.upper()
text_len = len(text)

key = 'KING'
key_len = len(key)

def new_shape(data, key_len):
    return np.reshape(data, (key_len,-1), order='F')

def add_filler(data, key_len, mod):
    temp = np.empty((key_len-mod), dtype=int)
    temp.fill(26)
    return np.append(data, temp)

def strided_app(a, L, S ):  # Window len = L, Stride len/stepsize = S
    nrows = (a.size-L) // S + 1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a, shape=(nrows,L), strides=(S*n,n))


cipher = np.fromiter(text, dtype='c').view(np.int8) - 65
print(f'1 - {cipher.base}')
#key = np.fromiter(key, dtype='c').view(np.int8) - 65

mod = text_len % key_len
if mod:
    plain = add_filler(cipher, key_len, mod)
    print(f'3 - {plain.base}')
    plain = plain.reshape((key_len, -1), order='F')
else:
    plain = cipher.reshape((key_len, -1), order='F')
print(f'2 - {plain.base}')

plain = plain.swapaxes(0,1)
print(f'4 - {plain.base}')
plain = np.broadcast_to(plain, (26,)+plain.shape)
print(f'5 - {plain.base}')
#print(plain.shape)
key = np.zeros((26,1,key_len), dtype=int)
print(f'6 - {key.base}')
n = 0
key[:,0,n] = range(26)
print(f'7 - {key.base}')
start = perf_counter()
for _ in range(1):
    guess = np.mod(np.subtract(plain, key), 26)
    print(f'9 - {guess.base}')
    guess1 = guess.flatten()
    qg = npi.indices(names, qgrams, missing=length)
end = perf_counter()
print(f'8 - {guess1.base}')
#qgrams = strided_app(guess1, 4, 1)
#print(qgrams)
#print(qgrams.shape)
# print(guess1)
# print(guess1.shape)
# print(key)
# print(guess)
#print(key.shape)

#guess = (plain-key) % 26


print(f'{end-start}s')