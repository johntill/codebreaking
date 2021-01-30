import itertools
import random
from time import perf_counter
import cipher_tools as tools

cipher_file = 'texts/Code_texts/ctkey12cipherICT.txt'
ev_file = 'texts/Frequencies/english_bigrams.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = tools.import_cipher(cipher_file)

key_len = 12

def decipher(text, key):
    ord_key = set(key)
    plain = [None] * text_len
    x = 0
    for char in ord_key:
        i = key.index(char)
        if i < num_long_col:
            new_col = full_rows + 1
        else:
            new_col = full_rows
        plain[i::key_len] = text[x:x + new_col]
        x += new_col
    return ''.join(plain)

def calculate_pos_min_max():
    # calculates the minimum and maximum starting positions
    # in the text for each column
    num_short_col = key_len - num_long_col
    adj = [None] * key_len
    for x in range(key_len):
        pos_min = x * full_rows
        pos_max = pos_min + min(x, num_long_col)
        if x > num_short_col:
            pos_min += x - num_short_col
        adj[x] = (pos_min, pos_max)
    return adj

def score_bigram(column_i, column_j):
    score = 0
    for char_a, char_b in zip(column_i, column_j):
        bigram = char_a + char_b
        if bigram in bigrams:
            score += bigrams[bigram]
        else:
            score += floor
    return score

def bi_score(text):

    adj = calculate_pos_min_max()
        
    scores = {}
    offset = {}
    col_len = full_rows + 1
    column_combos = itertools.permutations(range(key_len), 2)
    for i, j in column_combos:
        pos_min_i, pos_max_i = adj[i]
        pos_min_j, pos_max_j = adj[j]
        for pos_i in range(pos_min_i, pos_max_i + 1):
            for pos_j in range(pos_min_j, pos_max_j + 1):
                off = abs(pos_j - pos_i) % full_rows
                if off <= num_long_col:
                    column_i = text[pos_i:pos_i+col_len]
                    column_j = text[pos_j:pos_j+col_len]

                    total_score = score_bigram(column_i, column_j)
                    if (i, j) in scores:
                        if total_score > scores[(i, j)]:
                            scores[(i, j)] = total_score
                            offset[(i, j)] = off
                    else:
                        scores[(i, j)] = total_score
                        offset[(i, j)] = off
    return scores, offset

def adj_score(key):
    score = 0
    for x in range(key_len-1):
        i, j = key[x], key[x+1]
        score += scores[(i, j)]
    return score

def align_score(key):
    long_columns = key[:num_long_col]
    align, count = 0, 0
    for x in range(key_len-1):
        i, j = key[x], key[x+1]
        k, l = sorted((i,j))
        col = 0
        for c in range(k, l):
            if c in long_columns:
                col += 1
        if col == offset[(i, j)]:
            align += 2
            if count > 0:
                align += 1
            count += 1
        else:
            count = 0
    return align

attempts = 10
passed = 0

start = perf_counter()
for _ in range(attempts):
    bigrams, _, floor, _ = tools.create_ngram_attributes(ev_file, 1)
    text_len = len(text)
    full_rows = int(text_len / key_len)
    num_long_col = text_len % key_len
    full_rows, num_long_col = divmod(text_len, key_len)
    # sets the maximum possible align score
    max_align = (key_len - 1) * 3 - 1
    sequence = list(range(key_len))

    scores, offset = bi_score(text)

    best_key = tuple(random.sample(sequence, key_len))
    best_score = adj_score(best_key) - 100
    best_align = align_score(best_key)

    flag = True
    stage = 0
    while flag:
        flag = False
        stage += 1
        #print(stage)
        key = [*best_key]
        for l in range(1, key_len):
            for p in range(0, key_len - l):
                for s in range(1, key_len - l - p + 1):
                    new_key = key[0:p] + key[p+l:]
                    new_key = new_key[0:p+s] + key[p:p+l] + new_key[p+s:]
                    new_score = adj_score(new_key)
                    if new_score > best_score:
                        align = align_score(new_key)
                        if align > best_align - 3:
                            best_score, best_key = new_score, [*new_key]
                            best_align = align
                            flag = True

        key = [*best_key]
        for l in range(1, int(key_len / 2) + 1):
            for p1 in range(0, key_len - 2 * l + 1):
                for p2 in range(p1 + l, key_len - l + 1):
                    new_key = [*key]
                    new_key[p1:p1+l], new_key[p2:p2+l] = (new_key[p2:p2+l],
                                                        new_key[p1:p1+l])
                    new_score = adj_score(new_key)
                    if new_score > best_score:
                        align = align_score(new_key)
                        if align > best_align - 3:
                            best_score, best_key = new_score, [*new_key]
                            best_align = align
                            flag = True
    
        #print(best_align, best_score)
        key = [*best_key]
        for l in range(1, key_len):
            if align == max_align:
                break
            for p in range(0, key_len - l):
                for s in range(1, key_len - l - p + 1):
                    new_key = key[0:p] + key[p+l:]
                    new_key = new_key[0:p+s] + key[p:p+l] + new_key[p+s:]
                    align = align_score(new_key)
                    if align > best_align:
                        new_score = adj_score(new_key)
                        if new_score > new_score - 10:
                            best_score, best_key = new_score, [*new_key]
                            best_align = align
                            flag = True

        key = [*best_key]
        for l in range(1, int(key_len / 2) + 1):
            if align == max_align:
                break
            for p1 in range(0, key_len - 2 * l + 1):
                for p2 in range(p1 + l, key_len - l + 1):
                    new_key = [*key]
                    new_key[p1:p1+l], new_key[p2:p2+l] = (new_key[p2:p2+l],
                                                        new_key[p1:p1+l])
                    align = align_score(new_key)
                    if align > best_align:
                        new_score = adj_score(new_key)
                        if new_score > new_score - 10:
                            best_score, best_key = new_score, [*new_key]
                            best_align = align
                            flag = True
    
        #print(best_align, best_score)
        if stage == 30:
            break

    plain_text = decipher(text, best_key)
    # print(best_key)
    # print(plain_text)
    # print(best_align, best_score)

    attributes = tools.create_ngram_attributes(ngram_file, text_len)
    score_text = tools.ngram_score_text
    best_score = score_text(plain_text, attributes)

    flag = True
    while flag:
        flag = False
        key = [*best_key]
        for l in range(1, key_len):
            for p in range(0, key_len - l):
                for s in range(1, key_len - l - p + 1):
                    new_key = key[0:p] + key[p+l:]
                    new_key = new_key[0:p+s] + key[p:p+l] + new_key[p+s:]
                    plain_text = decipher(text, new_key)
                    candidate_score = score_text(plain_text, attributes)
                    if candidate_score > best_score:
                        best_score, best_key = candidate_score, [*new_key]
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break
        key = [*best_key]
        for l in range(1, int(key_len / 2) + 1):
            for p1 in range(0, key_len - 2 * l + 1):
                for p2 in range(p1 + l, key_len - l + 1):
                    new_key = [*key]
                    new_key[p1:p1+l], new_key[p2:p2+l] = (new_key[p2:p2+l],
                                                        new_key[p1:p1+l])
                    plain_text = decipher(text, new_key)
                    candidate_score = score_text(plain_text, attributes)
                    if candidate_score > best_score:
                        best_score, best_key = candidate_score, [*new_key]
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break

    #key = [*best_key]
    #key = key[1:] + key[0:1]
    #plain_text = decipher(text, key)
    #candidate_score = quad_fitness.score(plain_text)
    #if candidate_score > best_score:
    #    best_score = candidate_score
    #    best_key = [*key]

    # plain_text = decipher(text, best_key)
    # print(best_key)
    # print(plain_text)
    # print(best_score)
    if best_score > -9842:
        passed += 1

end = perf_counter()
print(f'Passed {passed}/{attempts} = {passed/attempts*100}')
time_taken = end - start
print(f'Time taken - {time_taken:.2f}s = {time_taken/attempts:.2f}s')
