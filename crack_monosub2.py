import re
import random
import time
import cipher_tools as tools

cipher_file = 'texts/Code_texts/subtest3.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

cipher_text = tools.import_cipher(cipher_file)
text_len = len(cipher_text)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_sequence = [*range(len(alphabet))]

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

best_score = -10_000_000

attempts = 1000
successes = 0
start = time.perf_counter()
for _ in range(attempts):
    current_key = [*alphabet]
    random.shuffle(current_key)
    plain_text = decrypt(cipher_text, current_key)
    current_score = score_text(plain_text, attributes)
    no_improvement = 0
    while no_improvement < 2300:
        key = swap_letters(current_key, alphabet_sequence)
        plain_text = decrypt(cipher_text, key)
        candidate_score = score_text(plain_text, attributes)
        if candidate_score > current_score:
            current_score, current_key = candidate_score, [*key]
            no_improvement = 0
        else:
            no_improvement += 1

    if current_score > best_score:
        best_score, best_key = current_score, [*current_key]

    # if current_score > -3282:
    #     successes += 1

end = time.perf_counter()

best_key = ''.join(best_key)
print(f'Best key - {best_key}')
plain_text = decrypt(cipher_text, best_key)
print(plain_text)
print(best_score)
print(f'Success rate = {successes/attempts*100}%')

time_taken = end - start
print(f'{time_taken:.2f}s - {time_taken/attempts:.2f}s')
