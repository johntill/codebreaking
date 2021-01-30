# Proof of concept implementation of decrypting the Caesar Cipher using Numpy.
# This allows for a vectorised approach, testing all 26 possibilities at once.
# Not useful in practice as importing numpy takes longer than cracking the
# code without it.
# The actual decryption is quicker if the import time is ignored though.

from time import perf_counter
import numpy as np
import cipher_tools as tools

start = perf_counter()

cipher_file = 'texts/Code_texts/Caesartest1.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'

text = tools.import_cipher(cipher_file)
text_len = len(text)

# Loads the expected values into a numpy array and adjusts for text length.
ngrams_ev = np.zeros((1,26))
with open(ev_file, 'r', encoding='utf8', errors='ignore') as f:
    for line in f:
        key, _, count = line.partition(' ')
        ngrams_ev[0,ord(key)-65] = int(count)
N = ngrams_ev.sum(axis=1)
ngrams_ev = np.multiply(np.divide(ngrams_ev, N), text_len)

for _ in range(1):
    # Creates numpy array from text, shape = (text_len,)
    # Letters are converted to ascii then reduced by 65 (asccii value for 'A')
    # so 'A' = 0 and 'Z' = 25
    cipher = np.fromiter(text, dtype='c').view(np.int8) - 65
    # Expand array to 26 identical copies of cipher, shape = (26,text_len)
    cipher = np.broadcast_to(cipher, (26, text_len))
    # Creates range 0-25 representing all possible Caesar shifts
    shifts_1 = np.arange(26)
    # Step 1
    # Applies all 26 possible Caesar shifts to the cipher
    # i.e. adds 0 to all elements of first copy, 1 to second....25 to 26th
    # Uses mod function to account for the end of alphabet
    cipher_step_1 = np.mod(np.add(cipher, shifts_1[:, None]), 26)
    # Multiplies original shifts by 26
    shifts_2 = np.multiply(shifts_1, 26)
    # Step 2
    # Adds shifts_2 to cipher_step_1 and flattens the array into 1 dimension.
    # This allows the numbers to be separated into bins and the frequenices counted
    # for each cipher.
    cipher_step_2 = np.add(cipher_step_1, shifts_2[:, None]).flat
    results_1 = np.bincount(cipher_step_2, minlength=676)
    # Reshapes results array to (26, text_len) to give letter counts for each shift.
    results_1 = results_1.reshape((26, -1))
    # Calculates Chi Squared score for each decryption
    results_2 = np.square(np.subtract(results_1, ngrams_ev))
    results_3 = np.divide(results_2, ngrams_ev)
    chi_squared = results_3.sum(axis=1)
    # Picks the lowest chi squared score as the correct decryption
    best_shift = np.argmin(chi_squared)
    plain_text = cipher_step_1[best_shift] + 65
    plain_text1 = "".join([chr(item) for item in plain_text])

end = perf_counter()

print(plain_text1.lower())


print(f'{end-start}s')
