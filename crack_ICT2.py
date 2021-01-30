# import timeit

# code_to_test = """
import random
import itertools
import cipher_tools as tools
from time import perf_counter

key_len = 25

cipher_file = 'texts/Code_texts/ctkey25cipherICT.txt'
ev_file = 'texts/Frequencies/english_bigrams.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = tools.import_cipher(cipher_file)

def decipher(text, key, text_len, full_rows, num_long_col):
    ord_key = sorted(key)
    plain = [None] * text_len
    x = 0
    for char in ord_key:
        i = key.index(char)
        col_len = full_rows+1 if i < num_long_col else full_rows
        plain[i::key_len] = text[x:x + col_len]
        x += col_len
    return ''.join(plain)

def calculate_pos_min_max(key_len, full_rows, num_long_col):
    # calculates the minimum and maximum starting positions
    # in the text for each column
    num_short_col = key_len - num_long_col
    adj = {}
    for column_number in range(key_len):
        pos_min = column_number * full_rows
        pos_max = pos_min + min(column_number, num_long_col)
        if column_number > num_short_col:
            pos_min += column_number - num_short_col
        adj[column_number] = (pos_min, pos_max)
    return adj

def score_bigram(bigrams, column_i, column_j):
    score = 0
    for char_a, char_b in zip(column_i, column_j):
        try:
            score += bigrams[char_a+char_b]
        except:
            score += floor
    return score

def bi_score(text, key_len, full_rows, num_long_col, bigrams):
    # key_len, full_rows, num_long_col
    adj = calculate_pos_min_max(key_len, full_rows, num_long_col)
    # key_len
    column_combos = itertools.permutations(range(key_len), 2)

    # column_combos, adj, text, full_rows, num_long_col, bigrams
    scores = {}
    offset = {}
    for i, j in column_combos:
        pos_min_i, pos_max_i = adj[i]
        pos_min_j, pos_max_j = adj[j]
        for pos_i in range(pos_min_i, pos_max_i+1):
            column_i = text[pos_i:pos_i+full_rows+1]
            for pos_j in range(pos_min_j, pos_max_j+1):
                off = abs(pos_j - pos_i) % full_rows
                if off <= num_long_col:
                    column_j = text[pos_j:pos_j+full_rows+1]

                    total_score = score_bigram(bigrams, column_i, column_j)

                    if (i, j) in scores:
                        if total_score > scores[(i, j)]:
                            scores[(i, j)] = total_score
                            offset[(i, j)] = off
                    else:
                        scores[(i, j)] = total_score
                        offset[(i, j)] = off
    return scores, offset

def adj_score(key, key_len, scores):
    score = 0
    for x in range(key_len-1):
        i, j = key[x], key[x+1]
        score += scores[(i, j)]
    return score

def align_score(key, key_len, num_long_col, offset):
    long_columns = set(key[:num_long_col])
    align = count = 0
    for x in range(key_len-1):
        i, j = key[x], key[x+1]
        k, l = (j, i) if i > j else (i, j)
        columns = set(range(k, l))
        number_of_columns = len(long_columns & columns)
        if number_of_columns == offset[(i, j)]:
            align += 2
            if count > 0:
                align += 1
            count += 1
        else:
            count = 0
    return align

def segment_slide(fixed_key):
    for l in range(1, key_len):
        for p in range(key_len - l):
            key = fixed_key[0:p] + fixed_key[p+l:]
            segment = fixed_key[p:p+l]
            for s in range(1, key_len - l - p + 1):
                yield key[0:p+s] + segment + key[p+s:]

def segment_swap(fixed_key):
    for l in range(1, int(key_len / 2) + 1):
        for p1 in range(key_len - 2 * l + 1):
            for p2 in range(p1 + l, key_len - l + 1):
                key = [*fixed_key]
                key[p1:p1+l], key[p2:p2+l] = (key[p2:p2+l], key[p1:p1+l])
                yield key

attempts = 1
for threshold in range(0, 1, 1):
    start = perf_counter()
    passed = 0
    for _ in range(attempts):
        bigrams, _, floor, _ = tools.create_ngram_attributes(ev_file, 1)
        text_len = len(text)
        full_rows, num_long_col = divmod(text_len, key_len)
        # sets the maximum possible align score
        max_align = (key_len - 1) * 3 - 1

        scores, offset = bi_score(text, key_len, full_rows, num_long_col, bigrams)

        best_key = list(range(key_len))
        random.shuffle(best_key)
        best_score = adj_score(best_key, key_len, scores) - 20
        best_align = align_score(best_key, key_len, num_long_col, offset)
        functions = [segment_slide, segment_swap]
        flag = True
        stage = 0
        while flag:
            flag = False
            stage += 1
            #print(stage)
            for func in functions:
                for new_key in func(best_key):
                    new_score = adj_score(new_key, key_len, scores)
                    if new_score > best_score:
                        align = align_score(new_key, key_len, num_long_col, offset)
                        if align > best_align - 5:
                            best_score, best_key = new_score, [*new_key]
                            best_align = align
                            flag = True

            #print(best_align, best_score)

            for func in functions:
                for new_key in func(best_key):
                    if align == max_align:
                        break
                    align = align_score(new_key, key_len, num_long_col, offset)
                    if align > best_align:
                        new_score = adj_score(new_key, key_len, scores)
                        if new_score > new_score - 23:
                            best_score, best_key = new_score, [*new_key]
                            best_align = align
                            flag = True

            #print(best_align, best_score)
            if stage == 30:
                break

        plain_text = decipher(text, best_key, text_len, full_rows, num_long_col)
        # print(best_key)
        # print(plain_text)
        # print(best_align, best_score)

        attributes = tools.create_ngram_attributes(ngram_file, text_len)
        score_text = tools.ngram_score_text
        best_score = score_text(plain_text, attributes)

        flag = True
        while flag:
            flag = False
            for func in functions:
                for new_key in func(best_key):
                    plain_text = decipher(text, new_key, text_len, full_rows, num_long_col)
                    candidate_score = score_text(plain_text, attributes)
                    if candidate_score > best_score:
                        best_score, best_key = candidate_score, [*new_key]
                        flag = True

        key = best_key[1:] + best_key[0:1]
        plain_text = decipher(text, key, text_len, full_rows, num_long_col)
        candidate_score = score_text(plain_text, attributes)
        if candidate_score > best_score:
           best_score, best_key = candidate_score, [*key]
           best_key = [*key]

        plain_text = decipher(text, best_key, text_len, full_rows, num_long_col)
        print(best_key)
        print(plain_text)
        print(best_score)
        if best_score > -9842:
            passed += 1

    end = perf_counter()
    print(f'{threshold} - Passed {passed}/{attempts} = {passed/attempts*100}% - {end-start}s')

