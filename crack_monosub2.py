import random
import cipher_tools as tools
from time import perf_counter

cipher_file = 'texts/Code_texts/subtest4.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

cipher_text = tools.import_cipher(cipher_file)
text_len = len(cipher_text)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_sequence = [*range(len(alphabet))]

def letter_expected_values(ev_file, alphabet):
    ngrams_ev = {}
    for line in open(ev_file, 'r'):
        key, _, count = line.partition(' ')
        if key in alphabet:
            ngrams_ev[key] = float(count)
    for char in alphabet:
        if char not in ngrams_ev:
            ngrams_ev[char] = 0
    count_total = sum(ngrams_ev.values())
    for ngram, score in ngrams_ev.items():
        ngrams_ev[ngram] = score / count_total
    return ngrams_ev

def set_key(frequencies, ev_list, alphabet):
    key_list = sorted(frequencies, key=frequencies.get, reverse=True)   
    key_list = ''.join(key_list)
    table = str.maketrans(ev_list, key_list)
    return alphabet.translate(table)

def decrypt(cipher_text, key):
    key = ''.join(key)
    table = str.maketrans(key, alphabet)
    return cipher_text.translate(table)

# swap 2 letters at random, must be different
def swap_letters(old_key, letter_choices):
    key = [*old_key]
    x, y = random.sample(letter_choices, 2)
    key[y], key[x] = key[x], key[y]
    return key

attributes = tools.create_ngram_attributes(ngram_file, text_len)
score_text = tools.ngram_score_text

ngrams_ev = letter_expected_values(ev_file, alphabet)
ev_list = ''.join(sorted(ngrams_ev, key=ngrams_ev.get, reverse=True))
frequencies = tools.frequency_analysis(cipher_text, alphabet)

attempts = 10
iterations = 4500
target_score = -1103

best_score = -10_000_000
success = 0
start = perf_counter()
for _ in range(attempts):
    current_key = set_key(frequencies, ev_list, alphabet)
    plain_text = decrypt(cipher_text, current_key)
    current_score = score_text(plain_text, attributes)
    for i in range(iterations):
        key = swap_letters(current_key, alphabet_sequence)
        plain_text = decrypt(cipher_text, key)
        candidate_score = score_text(plain_text, attributes)
        if candidate_score > current_score:
            current_score, current_key = candidate_score, [*key]

    if current_score > best_score:
        best_score, best_key = current_score, [*current_key]

    if current_score > target_score:
        success += 1

end = perf_counter()

best_key = ''.join(best_key)
print(f'Best key - {best_key}')
plain_text = decrypt(cipher_text, best_key)
print(plain_text)
print(best_score)
print(f'Successes = {success} / {attempts} = {success/attempts*100}%')

time_taken = end - start
print(f'{time_taken:.2f}s - {time_taken/attempts:.2f}s')
