import timeit

code_to_test = """
# code to brute force Playfair cipher using simulated annealing

import itertools
import math
import random
import code_playfair as playfair
import cipher_tools as tools
import ngram_score as ns

cipher_file = 'texts/Code_texts/playtest2.txt'
ngram_file = 'texts/Frequencies/english_quintgrams.txt'

# imports scoring mechanism
fitness = ns.NgramScore(ngram_file)

# loads cipher text from file and converts to uppercase
cipher_text = tools.import_cipher(cipher_file)

# sets alphabet to generate initial random key
# note lack of 'J'
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
# sets sequence to use for generating random numbers
# needed to avoid trying to swap same element
alphabet_sequence = [*range(len(alphabet))]

# swap 2 letters at random
def swap_letters(key):
    x, y = random.sample(alphabet_sequence, 2)
    key[y], key[x] = key[x], key[y]
    return key

# swap 2 rows at random
def swap_rows(key):
    x, y = random.sample(alphabet_sequence[0:5], 2)
    x, y = (x * 5), (y * 5)
    key[y:y+5], key[x:x+5] = key[x:x+5], key[y:y+5]
    return key

# swap 2 columns at random
def swap_columns(key):
    x, y = random.sample(alphabet_sequence[0:5], 2)
    key[y::5], key[x::5] = key[x::5], key[y::5]
    return key

# creates mirror of key along top left to bottom right diagonal
def TL_BR_mirror(key):
    key[1:5], key[5::5] = key[5::5], key[1:5]
    key[7:10], key[11::5] = key[11::5], key[7:10]
    key[13:15], key[17::5] = key[17::5], key[13:15]
    key[19], key[23] = key[23], key[19]
    return key

# creates mirror of key along top right to bottom left diagonal
def TR_BL_mirror(key):
    key[0:4], key[24:4:-5] = key[24:4:-5], key[0:4]
    key[5:8], key[23:8:-5] = key[23:8:-5], key[5:8]
    key[10:12], key[22:12:-5] = key[22:12:-5], key[10:12]
    key[15], key[21] = key[21], key[15]
    return key

# creates mirror of key along vertical
def L_R_mirror(key):
    key[0::5], key[4::5] = key[4::5], key[0::5]
    key[1::5], key[3::5] = key[3::5], key[1::5]
    return key

# creates mirror of key along horizontal
def T_B_mirror(key):
    key[0:5], key[20:25] = key[20:25], key[0:5]
    key[5:10], key[15:20] = key[15:20], key[5:10]
    return key

def randomly_mutate(key, options):
    choice = random.randrange(0, 50)
    if choice in options:
        return options[choice](key)
    else:
        return swap_letters(key)

solutions = {}
results = []

options = ({0: T_B_mirror, 1: L_R_mirror, 2: TR_BL_mirror, 3: TL_BR_mirror,
            4: swap_columns, 5: swap_columns, 6: swap_rows, 7: swap_rows})

for number in range(1, 10):
    print(f'Number: {number:02}')
    # sets initial temperature for simulated annealing
    T = 8
    stages = 0
    best_stage = 0
    blank_stages = 0
# creates random initial key from alphabet
    best_key = random.sample(alphabet, 25)
    plain_text = playfair.Playfair(best_key).decipher(cipher_text)
    best_score = fitness.score(plain_text)

#    while T > 0:
#    while best_score < -2956 and stages < 20:
    while stages < 50:
        stages += 1
        print(f"Stage: {stages}, Blank Stages: {blank_stages}")
        current_key = [*best_key]
        plain_text = playfair.Playfair(current_key).decipher(cipher_text)
        current_score = fitness.score(plain_text)

        for i in range(9999):
            # performs random transformation of current key
            key = randomly_mutate([*current_key], options)
            plain_text = playfair.Playfair(key).decipher(cipher_text)
            candidate_score = fitness.score(plain_text)
            delta_score = current_score - candidate_score
            if delta_score < 0 or math.exp(-delta_score / T) > 0.0085:
                current_score, current_key = candidate_score, [*key]
            if current_score > best_score:
                best_score, best_key = current_score, [*current_key]
                flag = True
                blank_stages = -1
                # if a new best score is found, perform all swaps
                # letters, then rows, then columns until no improvement
                while flag:
                    iter1 = itertools.combinations(range(25),2)
                    iter2 = itertools.combinations(range(0,25,5),2)
                    iter3 = itertools.combinations(range(5),2)
                    flag = False
                    # cycles through all letter swaps sequentially
                    for x, y in iter1:
                        key = [*best_key]
                        key[y], key[x] = key[x], key[y]
                        plain_text = playfair.Playfair(key).decipher(cipher_text)
                        candidate_score = fitness.score(plain_text)
                        if candidate_score > best_score:
                            best_score, best_key = candidate_score, [*key]
                            flag = True
                            break

                    # cycles through all row swaps sequentially
                    for x, y in iter2:
                        key = [*best_key]
                        key[y:y+5], key[x:x+5] = key[x:x+5], key[y:y+5]
                        plain_text = playfair.Playfair(key).decipher(cipher_text)
                        candidate_score = fitness.score(plain_text)
                        if candidate_score > best_score:
                            best_score, best_key = candidate_score, [*key]
                            flag = True
                            break

                    # cycles through all column swaps sequentially
                    for x, y in iter3:
                        key = [*best_key]
                        key[y::5], key[x::5] = key[x::5], key[y::5]
                        plain_text = playfair.Playfair(key).decipher(cipher_text)
                        candidate_score = fitness.score(plain_text)
                        if candidate_score > best_score:
                            best_score, best_key = candidate_score, [*key]
                            flag = True
                            break
                    
                    best_stage = stages

                key = ''.join(best_key)
                for i in range(0, 25, 5):
                    print(key[i:i+5])
                plain_text = playfair.Playfair(key).decipher(cipher_text)
                print(plain_text)
                print(best_score)
                print(T)
                
        #T -= 0.2
        blank_stages += 1
        # if blank_stages == 3:
        #     break
            
    solutions[number] = best_key
    results.append((number, best_stage, best_score))

for number, key in solutions.items():
    print(f'Solution: {number:02}')
    key = ''.join(key)
    plain_text = playfair.Playfair(key).decipher(cipher_text)
    for i in range(0, 25, 5):
        print(key[i:i+5])
    print(plain_text)
    print()

for (number, best_stage, best_score) in results:
    print(f"{number:02} = Best Stage: {best_stage:02} - Best Score: {best_score}")

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
