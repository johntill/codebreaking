import timeit

code_to_test = """
# code to brute force Playfair cipher using simulated annealing

import itertools
import math
import random
import code_playfair as playfair
import cipher_tools as tools

cipher_file = 'texts/Code_texts/TCB Stage6.txt'
ngram_file = 'texts/Frequencies/english_quintgrams.txt'

# loads cipher text from file and converts to uppercase
text = tools.import_cipher(cipher_file)
text_len = len(text)

# creates variables for scoring plain texts
attributes = tools.create_ngram_attributes(ngram_file, text_len)
# sets function for scoring plain texts
score_text = tools.ngram_score_text

# sets alphabet to generate initial random key
# note lack of 'J'
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def swap_all_elements(key):
    perms = itertools.combinations(range(25),2)
    for x, y in perms:
        new_key = [*key]
        new_key[x], new_key[y] = key[y], key[x]
        yield new_key

def swap_all_rows(key):
    perms = itertools.permutations(range(0,25,5),5)
    new_key = [None] * 25
    for perm in perms:
        for index, value in enumerate(perm):
            new_key[index*5:index*5+5] = key[value:value+5]
        yield new_key

def swap_all_columns(key):
    perms = itertools.permutations(range(5),5)
    new_key = [None] * 25
    for perm in perms:
        for index, value in enumerate(perm):
            new_key[index::5] = key[value::5]
        yield new_key

def swap_row_elements(key):
    for i in range(0,25,5):
        new_key = [*key]
        perms = itertools.permutations(range(5),5)
        for perm in perms:
            for index, value in enumerate(perm):
                new_key[i+index] = key[i+value]
            yield new_key

def swap_column_elements(key):
    for i in range(5):
        new_key = [*key]
        perms = itertools.permutations(range(0,25,5),5)       
        for perm in perms:
            for index, value in enumerate(perm):
                new_key[i+index*5] = key[i+value]
            yield new_key

# creates mirror of key along top left to bottom right diagonal
def TL_BR_mirror(key):
    key[1:5], key[5::5] = key[5::5], key[1:5]
    key[7:10], key[11::5] = key[11::5], key[7:10]
    key[13:15], key[17::5] = key[17::5], key[13:15]
    key[19], key[23] = key[23], key[19]
    yield key

# creates mirror of key along top right to bottom left diagonal
def TR_BL_mirror(key):
    key[0:4], key[24:4:-5] = key[24:4:-5], key[0:4]
    key[5:8], key[23:8:-5] = key[23:8:-5], key[5:8]
    key[10:12], key[22:12:-5] = key[22:12:-5], key[10:12]
    key[15], key[21] = key[21], key[15]
    yield key

# creates mirror of key along vertical
def L_R_mirror(key):
    key[0::5], key[4::5] = key[4::5], key[0::5]
    key[1::5], key[3::5] = key[3::5], key[1::5]
    yield key

# creates mirror of key along horizontal
def T_B_mirror(key):
    key[0:5], key[20:25] = key[20:25], key[0:5]
    key[5:10], key[15:20] = key[15:20], key[5:10]
    yield key

def print_key(key):
    show_key = ''.join(key)
    for i in range(0, 25, 5):
        print(show_key[i:i+5])
    print()

def accept_number(new_score, current_score, fixed_temp):
    if new_score > current_score:
        return True
    #fixed_temp = 10
    degradation = current_score - new_score
    acceptance_probability = math.exp(-degradation / fixed_temp)
    return acceptance_probability > 0.0085 and random.random() < acceptance_probability

options = ([swap_all_elements, swap_all_rows, swap_all_columns,
            swap_row_elements, swap_column_elements])
            #TL_BR_mirror, TR_BL_mirror, L_R_mirror, T_B_mirror])

solutions = {}
results = []

# sets initial temperature for simulated annealing
T = 27

for number in range(1, 4):
    print(f'Number: {number:02}')
    stages = blank_stages = 0
    # creates random initial key from alphabet
    best_key = list(alphabet)
    random.shuffle(best_key)
    plain_text = playfair.Playfair(best_key).decipher(text)
    best_score = score_text(plain_text, attributes)

    while best_score < -3517 and stages < 100:
        stages += 1
        #print(f"Stage: {stages}, Blank Stages: {blank_stages}")
        current_key = [*best_key]
        plain_text = playfair.Playfair(current_key).decipher(cipher_text)
        current_score = score_text(plain_text, attributes)
        for option in options:
            for key in option(current_key):
                plain_text = playfair.Playfair(key).decipher(text)
                new_score = score_text(plain_text, attributes)
                accept = accept_number(new_score, current_score, T)
                #delta_score = current_score - new_score
                #if delta_score < 0 or math.exp(-delta_score / T) > 0.0085:
                if accept:
                    current_score, current_key = new_score, [*key]
                    #print(plain_text)
                if current_score > best_score:
                    best_score, best_key = current_score, [*current_key]
                    best_stage = stages
                    blank_stages = -1
                    #print_key(best_key)
                    #print(plain_text)
                    #print(best_score)
                    break
        blank_stages += 1
    solutions[number] = best_key
    results.append((number, best_stage, best_score))

# for number, key in solutions.items():
#     print(f'Solution: {number:02}')
#     print_key(key)
#     plain_text = playfair.Playfair(key).decipher(text)
#     print(plain_text)
#     print()

for (number, best_stage, best_score) in results:
    print(f"{number:02} = Best Stage: {best_stage:02} - Best Score: {best_score}")

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
