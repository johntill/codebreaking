# Checks all key lengths from 2-15 for CCT
# CCT = Complete Columnar Transposition
# i.e. all columns are the same length
# change which key lengths are checked at line 84
# choose Bigram or Trigram scoring at lines 92 & 93

import itertools
import random
import re
import time
import ngram_score as ns

quad_fitness = ns.NgramScore('texts/Frequencies/english_quadgrams.txt')

with open('texts/Code_texts/ctkey15shortCCT.txt') as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())
text_len = len(text)

def decipher(text, key):
    ord_key = sorted(key)
    plain = [None] * text_len
    x = 0
    for char in ord_key:
        i = key.index(char)
        new_col = rows + 1 if i < rem else rows
        plain[i::key_len] = text[x:x + new_col]
        x += new_col
    return ''.join(plain)

def bi_score(text):
    scores = {}
    bi_fitness = ns.NgramScore('texts/Frequencies/english_bigrams.txt')
    iter_bi = itertools.permutations(range(key_len), 2)
    for i, j in iter_bi:
        column_i = text[i*rows:i*rows+rows]
        column_j = text[j*rows:j*rows+rows]
        total_score = sum(bi_fitness.score(a + b) for a, b in zip(column_i, column_j))
        scores[(i, j)] = total_score
    return scores

def tri_score(text):
    scores = {}
    tri_fitness = ns.NgramScore('texts/Frequencies/english_trigrams.txt')
    iter_tri = itertools.permutations(range(key_len), 3)
    for i, j, k in iter_tri:
        column_i = text[i*rows:(i*rows+rows)]
        column_j = text[j*rows:(j*rows+rows)]
        column_k = text[k*rows:(k*rows+rows)]
        total_score = sum(
            tri_fitness.score(a + b + c)
            for a, b, c in zip(column_i, column_j, column_k)
        )
        if (i, j) in scores:
            if total_score > scores[(i, j)]:
                scores[(i, j)] = total_score
        else:
            scores[(i, j)] = total_score
    return scores


attempts = 1
passed = 0

start = time.perf_counter()
for _ in range(attempts):
    record_score = -10_000_000

    # checks key length 2
    iter = itertools.permutations(range(2), 2)
    key_len = 2
    rows = int(text_len / key_len)
    rem = text_len % key_len
    for item in iter:
        plain_text = decipher(text, item)
        candidate_score = quad_fitness.score(plain_text)
        if candidate_score > record_score:
            record_score = candidate_score
            record_key = [*item]
    
    # Set range of key lengths to be checked
    # Minimum length cannot be < 3
    for key_len in range(3, 16):
        best_bigram_score = best_score = -10_000_000
        rows = int(text_len / key_len)
        rem = text_len % key_len
        sequence = list(range(key_len))

        # CHOOSE SCORING METHOD
        # Bigram is faster, Trigram is potentially more accurate.
        # Comment out the option you don't wish to use
        scores = bi_score(text)
        #scores = tri_score(text)

        current_key = random.sample(sequence, key_len)
        current_score = 0
        for x in range(key_len-1):
            i, j = current_key[x], current_key[x+1]
            current_score += scores[(i, j)]
        if current_score > best_bigram_score:
            best_bigram_score = current_score
            best_key = [*current_key]

        flag = True
        while flag:
            flag = False
            key = [*best_key]
            for l in range(1, key_len):
                for p in range(key_len - l):
                    for s in range(1, key_len - l - p + 1):
                        new_key = key[0:p] + key[p+l:]
                        new_key = new_key[0:p+s] + key[p:p+l] + new_key[p+s:]
                        new_score = 0
                        for x in range(key_len-1):
                            i, j = new_key[x], new_key[x+1]
                            new_score += scores[(i, j)]
                        if new_score > best_bigram_score:
                            best_score = new_score
                            best_key = [*new_key]
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    break
        
        print(key_len, best_score)
        plain_text = decipher(text, best_key)
        best_score = quad_fitness.score(plain_text)

        flag = True
        while flag:
            flag = False
            key = [*best_key]
            for l in range(1, key_len):
                for p in range(key_len - l):
                    for s in range(1, key_len - l - p + 1):
                        new_key = key[0:p] + key[p+l:]
                        new_key = new_key[0:p+s] + key[p:p+l] + new_key[p+s:]
                        plain_text = decipher(text, new_key)
                        candidate_score = quad_fitness.score(plain_text)
                        if candidate_score > best_score:
                            best_score = candidate_score
                            best_key = [*new_key]
                            flag = True
                            break
                    if flag:
                        break
                if flag:
                    break

        if best_score > record_score:
            record_score = best_score
            record_key = [*best_key]

    key = [*record_key]
    key_len = len(record_key)
    rows = int(text_len / key_len)
    rem = text_len % key_len
    key = key[1:] + key[0:1]
    plain_text = decipher(text, key)
    candidate_score = quad_fitness.score(plain_text)
    if candidate_score > record_score:
        record_score = candidate_score
        record_key = [*key]

    if record_score > -575:
        passed += 1    

plain_text = decipher(text, record_key)
print(record_key, plain_text)
print(record_score)

end = time.perf_counter()
print(f'Passed - {passed}/{attempts} = {passed/attempts*100}%')
time_taken = end - start
print(f'Time taken - {time_taken:.2f}s = {time_taken/attempts:.2f}s')
