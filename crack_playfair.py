# code to brute force Playfair cipher using simulated annealing

from time import perf_counter
import itertools
import math
import random
import code_playfair as playfair
import cipher_tools as tools


cipher_file = 'texts/Code_texts/TCB Stage6.txt'
ngram_file = 'texts/Frequencies/english_quintgrams.txt'

# loads cipher text from file and converts to uppercase
cipher_text = tools.import_cipher(cipher_file)
text_len = len(cipher_text)

# creates variables for scoring plain texts
attributes = tools.create_ngram_attributes(ngram_file, text_len)
# sets function for scoring plain texts
score_text = tools.ngram_score_text

# sets alphabet to generate initial random key
# note lack of 'J'
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
# sets sequence to use for generating random numbers
# needed to avoid trying to swap same element
alphabet_sequence = [*range(len(alphabet))]

# swap 2 letters at random
def swap_letters(old_key):
    key = [*old_key]
    x, y = random.sample(alphabet_sequence, 2)
    key[y], key[x] = key[x], key[y]
    return key

# swap 2 rows at random
def swap_rows(old_key):
    key = [*old_key]
    x, y = random.sample(alphabet_sequence[0:5], 2)
    x, y = (x * 5), (y * 5)
    key[y:y+5], key[x:x+5] = key[x:x+5], key[y:y+5]
    return key

# swap 2 columns at random
def swap_columns(old_key):
    key = [*old_key]
    x, y = random.sample(alphabet_sequence[0:5], 2)
    key[y::5], key[x::5] = key[x::5], key[y::5]
    return key

# creates mirror of key along top left to bottom right diagonal
def TL_BR_mirror(old_key):
    key = [*old_key]
    key[1:5], key[5::5] = key[5::5], key[1:5]
    key[7:10], key[11::5] = key[11::5], key[7:10]
    key[13:15], key[17::5] = key[17::5], key[13:15]
    key[19], key[23] = key[23], key[19]
    return key

# creates mirror of key along top right to bottom left diagonal
def TR_BL_mirror(old_key):
    key = [*old_key]
    key[0:4], key[24:4:-5] = key[24:4:-5], key[0:4]
    key[5:8], key[23:8:-5] = key[23:8:-5], key[5:8]
    key[10:12], key[22:12:-5] = key[22:12:-5], key[10:12]
    key[15], key[21] = key[21], key[15]
    return key

# creates mirror of key along vertical
def L_R_mirror(old_key):
    key = [*old_key]
    key[0::5], key[4::5] = key[4::5], key[0::5]
    key[1::5], key[3::5] = key[3::5], key[1::5]
    return key

# creates mirror of key along horizontal
def T_B_mirror(old_key):
    key = [*old_key]
    key[0:5], key[20:25] = key[20:25], key[0:5]
    key[5:10], key[15:20] = key[15:20], key[5:10]
    return key

def reverse_key(key):
    return key[::-1]

def randomly_mutate(key, options):
    choice = random.randrange(0, 50)
    if choice in options:
        return options[choice](key)
    else:
        return swap_letters(key)

def swap_all_elements(old_key):
    perms = itertools.combinations(range(25),2)
    for x, y in perms:
        key = [*old_key]
        key[x], key[y] = key[y], key[x]
        yield key

def swap_all_rows(old_key):
    perms = itertools.permutations(range(0,25,5),5)
    key = [None] * 25
    for perm in perms:
        for index, value in enumerate(perm):
            key[index*5:index*5+5] = old_key[value:value+5]
        yield key

def swap_all_columns(old_key):
    perms = itertools.permutations(range(5),5)
    key = [None] * 25
    for perm in perms:
        for index, value in enumerate(perm):
            key[index::5] = old_key[value::5]
        yield key

def swap_row_elements(old_key):
    for i in range(0,25,5):
        key = [*old_key]
        perms = itertools.permutations(range(5),5)
        for perm in perms:
            for index, value in enumerate(perm):
                key[i+index] = old_key[i+value]
            yield key

def swap_column_elements(old_key):
    for i in range(5):
        key = [*old_key]
        perms = itertools.permutations(range(0,25,5),5)       
        for perm in perms:
            for index, value in enumerate(perm):
                key[i+index*5] = old_key[i+value]
            yield key

def swap_4_letter_groups(old_key):
    key_len = len(old_key)
    for s in range(key_len-7):
        s1 = old_key[s:s+4]
        for p in range(s+4, key_len-3):
            key = [*old_key]
            p1 = old_key[p:p+4]
            key[s:s+4], key[p:p+4] = p1, s1
            yield key

def print_key(key):
    show_key = ''.join(key)
    for i in range(0, 25, 5):
        print(show_key[i:i+5])
    print()

def accept_number(new_score, current_score, fixed_temp):
    if new_score > current_score:
        return True
    degradation = current_score - new_score
    acceptance_probability = math.exp(-degradation / fixed_temp)
    return acceptance_probability > 0.0085 and random.random() < acceptance_probability

option_choices = ({T_B_mirror: [0], L_R_mirror: [1], TR_BL_mirror: [2, 3],
                   swap_columns: [4, 5], swap_rows: [6, 7]})

options = {value: key for key in option_choices for value in option_choices[key]}

systematic_options = ([swap_all_elements, swap_all_rows, swap_all_columns,
                       swap_row_elements, swap_column_elements,
                       swap_4_letter_groups])


# sets initial temperature for simulated annealing
T = 27
solutions = {}
results = []
successes = 0
for number in range(1, 3):
    start = perf_counter()
    #print(f'Number: {number:02}')
    stages = blank_stages = 0
    # creates random initial key from alphabet
    best_key = [*alphabet]
    random.shuffle(best_key)
    plain_text = playfair.Playfair(best_key).decipher(cipher_text)
    best_score = score_text(plain_text, attributes)
    
#    while T > 0:
    while best_score < -3517 and stages < 16: # -2956 quadgrams
#    while stages < 20:
        stages += 1
        current_key = [*best_key]
        plain_text = playfair.Playfair(current_key).decipher(cipher_text)
        current_score = score_text(plain_text, attributes)
        #print(f"Stage: {stages}, Blank Stages: {blank_stages}")
        for i in range(9999):
            # performs random transformation of current key
            key = randomly_mutate(current_key, options)
            plain_text = playfair.Playfair(key).decipher(cipher_text)
            candidate_score = score_text(plain_text, attributes)
            accept = accept_number(candidate_score, current_score, T)
            if accept:
                current_score, current_key = candidate_score, [*key]
            if current_score > best_score:
                best_score, best_key = current_score, [*current_key]
                flag = True
                blank_stages = -1
                # if a new best score is found, perform all swaps
                # letters, then rows, then columns until no improvement
                while flag:
                    flag = False
                    for func in systematic_options:
                        for key in func(best_key):
                            plain_text = playfair.Playfair(key).decipher(cipher_text)
                            candidate_score = score_text(plain_text, attributes)
                            if candidate_score > best_score:
                                best_score, best_key = candidate_score, [*key]
                                flag = True
                                break

                    # # cycles through all letter swaps sequentially
                    # for key in swap_all_elements(best_key):
                    #     plain_text = playfair.Playfair(key).decipher(cipher_text)
                    #     candidate_score = score_text(plain_text, attributes)
                    #     if candidate_score > best_score:
                    #         best_score, best_key = candidate_score, [*key]
                    #         flag = True 
                    #         break
                    # # cycles through all row swaps sequentially
                    # for key in swap_all_rows(best_key):
                    #     plain_text = playfair.Playfair(key).decipher(cipher_text)
                    #     candidate_score = score_text(plain_text, attributes)
                    #     if candidate_score > best_score:
                    #         best_score, best_key = candidate_score, [*key]
                    #         flag = True
                    #         break
                    # # cycles through all column swaps sequentially
                    # for key in swap_all_columns(best_key):
                    #     plain_text = playfair.Playfair(key).decipher(cipher_text)
                    #     candidate_score = score_text(plain_text, attributes)
                    #     if candidate_score > best_score:
                    #         best_score, best_key = candidate_score, [*key]
                    #         flag = True
                    #         break

                best_stage = stages
                #print_key(best_key)
                #plain_text = playfair.Playfair(best_key).decipher(cipher_text)
                #print(plain_text)
                #print(best_score)
                #print(T)
                
        #T -= 0.2
        blank_stages += 1
            
    solutions[number] = best_key
    end = perf_counter()
    time_taken = end - start
    results.append((number, best_stage, best_score, time_taken))
    if best_score > -3517:
        successes += 1

# for number, key in solutions.items():
#     print(f'Solution: {number:02}')
#     print_key(key)
#     plain_text = playfair.Playfair(key).decipher(cipher_text)
#     print(plain_text)
#     print()

total_time = 0
print(f'Temp = {T} - Success = {successes/number*100:.2f}%')
for (number, best_stage, best_score, time_taken) in results:
    total_time += time_taken
    print(f'{number:02} = Best Stage: {best_stage:02} - Best Score: {best_score:.4f} - {time_taken:.2f}s')
print(f'Total time = {total_time:.2f}s or {total_time/number:.2f}s per attempt')
print()


