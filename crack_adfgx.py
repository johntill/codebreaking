import random
import itertools
import code_columnartransposition as ct
import code_polybius_square as ps
import cipher_tools as tools
import ngram_score as ns
from collections import defaultdict

cipher_file = 'texts/Code_texts/adfgvxshort24.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

# sets key length, if set to 1 will run section to
# determine length of key automatically
key_len = 1


cipher_text = tools.import_cipher(cipher_file)
text_len = len(cipher_text)

def score_key(key, ngram_size):
    plain_text = ct.ColumnarTransposition(key).decipher(cipher_text)
    n_grams = tools.ngram_freq_counter(plain_text, ngram_size, 2)
    IC = tools.calculate_IC(n_grams, text_len / 2)
    if IC > best_score:
        return [*key], IC, True
    return [*best_key], best_score, flag

#swaps 2 segments of various lengths and positions, all permutations
def segment_swap(fixed_key):
    for l in range(1, int(key_len / 2) + 1):
        for p1 in range(key_len - 2 * l + 1):
            for p2 in range(p1 + l, key_len - l + 1):
                key = [*fixed_key]
                key[p1:p1+l], key[p2:p2+l] = (key[p2:p2+l], key[p1:p1+l])
                yield key

# cut down version of main body
# runs optionally if key_length is set to 1 on line 19
# checks all key lengths 2 -> 25 to find correct length
# roughly 98% accurate

if key_len == 1:
    results = defaultdict(int)
    for _ in range(5):
        record_score = 0
        for key_len in range(2, 26):
            key_sequence = [*range(key_len)]
            best_score = 0
            for _ in range(100):
                key = random.sample(key_sequence, key_len)
                best_key, best_score, flag = score_key(key, 2)
            for key in segment_swap(best_key):
                best_key, best_score, flag = score_key(key, 2)
            if best_score > record_score:
                record_score, record_key = best_score, [*best_key]
        key_len = len(record_key)
        results[key_len] += record_score
    key_len = max(results, key=results.get)

print(f"Key length is {key_len}")

# swaps 2 elements, all permutations
def element_swap(fixed_key):
    permutations = itertools.combinations(range(key_len), 2)
    for x, y in permutations:
        key = [*fixed_key]
        key[y], key[x] = key[x], key[y]
        yield key

# slides segments of all lengths and starting positions
def segment_slide(fixed_key):
    for l in range(1, key_len):
        for p in range(key_len - l):
            key = fixed_key[0:p] + fixed_key[p+l:]
            segment = fixed_key[p:p+l]
            for s in range(1, key_len - l - p + 1):
                yield key[0:p+s] + segment + key[p+s:]

# rotate (cyclically) segments of all lengths and positions
def segment_rotate(fixed_key):
    for l in range(2, key_len + 1):
        for p in range(key_len + 1 - l):
            key = [*fixed_key]
            for _ in range(l-1):
                key[p:p+l] = key[p+l-1:p+l] + key[p:p+l-1]
                yield key
                                                                                                
# 1st part of program to undo transposition phase
# runs until quad_score is 0.0075 or greater
functions = [element_swap, segment_slide, segment_swap, segment_rotate]
key = list(range(key_len))
record_score = 0
rounds = 0
while record_score < 0.0075:
    rounds += 1
    best_score = 0
    # generates 10,000 initial keys and chooses 'best'
    for _ in range(10000):
        random.shuffle(key)
        best_key, best_score, flag = score_key(key, 4)
    flag = True
    while flag:
        flag = False
        for func in functions:
            for key in func(best_key):
                best_key, best_score, flag = score_key(key, 4)
        # reverses key
        key = best_key[::-1]
        best_key, best_score, flag = score_key(key, 4)
        # swaps the elements of each pair in key
        key = [*best_key]
        for x in range(0, key_len - 1, 2):
            key[x+1], key[x] = key[x], key[x+1]
            best_key, best_score, flag = score_key(key, 4)
    if best_score > record_score:
        record_score, record_key = best_score, [*best_key]
    print(f'{rounds:02} - {record_score}')

print(record_key)

# runs extra code but with record_key split into tuples
# this decreases number of transformations needed on longer keys
# needed as key space can be very large which requires a
# large number of attempts to find correct key for key length > 20
# set to run for max of 9 rounds to minimise wasted time on shorter keys
# but still be ~ 99.9% accurate on longer keys

best_score = record_score
key = list(zip(*[iter(record_key)]*2))
key_len = len(key)
for x in range(0, key_len - 1, 2):
     key[x+1], key[x] = key[x], key[x+1]
key = list(zip(*[iter(key)]*2))
key_len = len(key)
iter1 = itertools.permutations(key, key_len)
for new_key in iter1:
    new_key = [x for y in new_key for x in y]
    key_len = len(new_key)
    for x in range(0, key_len - 1, 2):
        key = [*new_key]
        key[x+1], key[x] = key[x], key[x+1]
        key = [x for y in key for x in y]
        best_key, best_score, flag = score_key(key, 4)
    if best_score > record_score:
        record_score, record_key = best_score, [*best_key]
        break

print(record_key)

print(record_score)
# undoes transposition using record key
phase2_text = ct.ColumnarTransposition(record_key).decipher(cipher_text)

# sets alphabet for inside key square
def set_alphabet(chars):
    if len(chars) == 5: # ADFGX
        return 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    elif len(chars) == 6: # ADFGVX
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

chars = ''.join(sorted(set(cipher_text)))
alphabet = set_alphabet(chars)

# undoes Polybius Square using alphabet as key
# so text is ready for substitution phase
cipher_text = ps.PolybiusSquare(alphabet, chars).decipher(phase2_text)

# 2nd part of program to undo substitution phase

def letter_expected_values(text_file, alphabet):
    ngrams_ev = {}
    for line in open(text_file, 'r'):
        key, _, count = line.partition(' ')
        if key in alphabet:
            ngrams_ev[key] = int(count)
    for char in alphabet:
        if char not in ngrams_ev:
            ngrams_ev[char] = 0
    ev_list = sorted(ngrams_ev, key=ngrams_ev.get)
    return ''.join(ev_list)

ev_list = letter_expected_values(ev_file, alphabet)
frequencies = tools.frequency_analysis(cipher_text, alphabet)
fitness = ns.NgramScore(ngram_file)
best_score = -10_000_000
# sets sequence for randomly swapping letters in mono-sub phase
alphabet_sequence = [*range(len(alphabet))]

def set_key(frequencies, ev_list):
    key_list = sorted(frequencies, key=frequencies.get)
    key_list = ''.join(key_list)
    table = str.maketrans(ev_list, key_list)
    return alphabet.translate(table)

def decrypt(cipher_text, key):
    key = ''.join(key)
    table = str.maketrans(key, alphabet)
    return cipher_text.translate(table)

# swap 2 letters at random, must be different
def swap_letters(key):
    x, y = random.sample(alphabet_sequence, 2)
    key[y], key[x] = key[x], key[y]
    return key

for _ in range(6):
    current_key = set_key(frequencies, ev_list)
    plain_text = decrypt(cipher_text, current_key)
    current_score = fitness.score(plain_text)
    for _ in range(6000):
        key = [*current_key]
        key = swap_letters(key)
        plain_text = decrypt(cipher_text, key)
        candidate_score = fitness.score(plain_text)
        if candidate_score > current_score:
            current_score, current_key = candidate_score, [*key]
    if current_score > best_score:
        best_score, best_key = current_score, [*current_key]

best_key = ''.join(best_key)
print(best_key)
plain_text = decrypt(cipher_text, best_key)
print(plain_text)
print(best_score)
