import timeit

code_to_test = """
import re
import random
import cipher_tools as ct

cipher_file = 'texts/Code_texts/subtest4.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

cipher_text = ct.import_cipher(cipher_file)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_sequence = list(range(len(alphabet)))

def letter_expected_values(ev_file, alphabet):
    ngrams_ev = {}
    for line in open(ev_file, 'r'):
        key, _, count = line.partition(' ')
        if key in alphabet:
            ngrams_ev[key] = count
    for char in alphabet:
        if char not in ngrams_ev:
            ngrams_ev[char] = 0
    ev_list = sorted(ngrams_ev, key=ngrams_ev.get)
    return ''.join(ev_list)

def set_key(frequencies, ev_list, alphabet):
    key_list = sorted(frequencies, key=frequencies.get)
    key_list = ''.join(key_list)
    table = str.maketrans(ev_list, key_list)
    return alphabet.translate(table)

def decrypt(cipher_text, key):
    key = ''.join(key)
    table = str.maketrans(key, alphabet)
    return cipher_text.translate(table)

# swap 2 letters at random, must be different
def swap_letters(key, alphabet_sequence):
    x, y = random.sample(alphabet_sequence, 2)
    key[y], key[x] = key[x], key[y]
    return key

ngram_attributes = ct.create_ngram_attributes(ngram_file, text_len)
ngram_score_text = ct.ngram_score_text
frequencies = ct.frequency_analysis(cipher_text, alphabet)
ev_list = letter_expected_values(ev_file, alphabet)
best_score = -10_000_000

for x in range(4):
    current_key = set_key(frequencies, ngrams_ev)
    plain_text = decrypt(cipher_text, current_key)
    current_score = ngram_score_text(plain_text, ngram_attributes)
    for i in range(4000):
        key = [*current_key]
        key = swap_letters(key)
        plain_text = decrypt(cipher_text, key)
        candidate_score = ngram_score_text(plain_text, ngram_attributes)
        if candidate_score > current_score:
            current_score, current_key = candidate_score, [*key]
    if current_score > best_score:
        best_score, best_key = current_score, [*current_key]

best_key = ''.join(best_key)
print(best_key)
plain_text = decrypt(cipher_text, best_key)
print(plain_text)
print(best_score)
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1
print(elapsed_time)
