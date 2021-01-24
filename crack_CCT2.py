# Checks all key lengths from 2-15 for CCT
# CCT = Complete Columnar Transposition
# i.e. all columns are the same length
# change which key lengths are checked at line 107
# choose Bigram or Trigram scoring at lines 21 & 22

import itertools
import random
import re
import time
import cipher_tools as tools

cipher_file = 'texts/Code_texts/ctkey12cipherICT.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

# CHOOSE SCORING METHOD
# Bigram is faster, Trigram is potentially more accurate.
# Comment out the option you don't wish to use
score_using = 'bigrams'
#score_using = 'trigrams'

text = tools.import_cipher(cipher_file)
text_len = len(text)

attributes = tools.create_ngram_attributes(ngram_file, text_len)
score_text = tools.ngram_score_text

def decipher(text, key):
    ord_key = sorted(key)
    plain = [None] * text_len
    x = 0
    for char in ord_key:
        i = key.index(char)
        col_len = full_rows+1 if i < num_long_col else full_rows
        plain[i::key_len] = text[x:x + col_len]
        x += col_len
    return ''.join(plain)

def set_scoring_method(score_using):
    scoring_function, ev_file = scoring_functions[score_using]
    ngrams, _, ngram_floor, _  = tools.create_ngram_attributes(ev_file, 1)
    return scoring_function, ngrams, ngram_floor

def score_bigrams(text, ngrams, ngram_floor):
    scores = {}
    iter_bi = itertools.permutations(range(key_len), 2)
    for i, j in iter_bi:
        column_i = text[i*full_rows:i*full_rows+full_rows]
        column_j = text[j*full_rows:j*full_rows+full_rows]
        score = 0
        for char_a, char_b in zip(column_i, column_j):
            try:
                score += ngrams[char_a + char_b]
            except:
                score += ngram_floor
        scores[(i, j)] = score
    return scores

def score_trigrams(text, ngrams, ngram_floor):
    scores = {}
    iter_tri = itertools.permutations(range(key_len), 3)
    for i, j, k in iter_tri:
        column_i = text[i*full_rows:i*full_rows+full_rows]
        column_j = text[j*full_rows:j*full_rows+full_rows]
        column_k = text[k*full_rows:k*full_rows+full_rows]
        score = 0
        for char_a, char_b, char_c in zip(column_i, column_j, column_k):
            try:
                score += ngrams[char_a + char_b + char_c]
            except:
                score += ngram_floor
        if (i, j) in scores:
            if score > scores[(i, j)]:
                scores[(i, j)] = score
        else:
            scores[(i, j)] = score
    return scores

def segment_slide(fixed_key):
    for l in range(1, key_len):
        for p in range(key_len - l):
            key = fixed_key[0:p] + fixed_key[p+l:]
            segment = fixed_key[p:p+l]
            for s in range(1, key_len - l - p + 1):
                yield key[0:p+s] + segment + key[p+s:]


scoring_functions = {
    'bigrams': (score_bigrams, 'texts/Frequencies/english_bigrams.txt'),
    'trigrams': (score_trigrams, 'texts/Frequencies/english_trigrams.txt')
}

attempts = 1
passed = 0

start = time.perf_counter()
for _ in range(attempts):
    record_score = -10_000_000

    # checks key length 2
    iter = itertools.permutations(range(2), 2)
    key_len = 2
    full_rows, num_long_col = divmod(text_len, key_len)
    for key in iter:
        plain_text = decipher(text, key)
        candidate_score = score_text(plain_text, attributes)
        if candidate_score > record_score:
            record_score = candidate_score
            record_key = [*key]

    scoring_function, ngrams, ngram_floor = set_scoring_method(score_using)

    # Set range of key lengths to be checked
    # Minimum length cannot be < 3
    for key_len in range(3, 16):
        full_rows, num_long_col = divmod(text_len, key_len)
        scores = scoring_function(text, ngrams, ngram_floor)

        best_key = list(range(key_len))
        random.shuffle(best_key)
        best_score = 0
        for x in range(key_len-1):
            i, j = best_key[x], best_key[x+1]
            best_score += scores[(i, j)]

        flag = True
        while flag:
            flag = False
            for new_key in segment_slide(best_key):
                new_score = 0
                for x in range(key_len-1):
                    i, j = new_key[x], new_key[x+1]
                    new_score += scores[(i, j)]
                if new_score > best_score:
                    best_score = new_score
                    best_key = [*new_key]
                    flag = True
                    break
        
        plain_text = decipher(text, best_key)
        best_score = score_text(plain_text, attributes)

        flag = True
        while flag:
            flag = False
            for new_key in segment_slide(best_key):
                plain_text = decipher(text, new_key)
                candidate_score = score_text(plain_text, attributes)
                if candidate_score > best_score:
                    best_score = candidate_score
                    best_key = [*new_key]
                    flag = True
                    break

        if best_score > record_score:
            record_score = best_score
            record_key = [*best_key]

    key = [*record_key]
    key_len = len(record_key)
    full_rows, num_long_col = divmod(text_len, key_len)
    key = key[1:] + key[0:1]
    plain_text = decipher(text, key)
    candidate_score = score_text(plain_text, attributes)
    if candidate_score > record_score:
        record_score = candidate_score
        record_key = [*key]
    
    if record_score > -9842:
        passed += 1

# plain_text = decipher(text, record_key)
# print(record_key, plain_text)
# print(record_score)

end = time.perf_counter()
print(f'Passed - {passed}/{attempts} = {passed/attempts*100}%')
time_taken = end - start
print(f'Time taken - {time_taken:.2f}s = {time_taken/attempts:.2f}s')
