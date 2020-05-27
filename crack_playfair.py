import timeit

code_to_test = """
# code to brute force Playfair cipher using simulated annealing

import re
import string
import random
import math
import code_playfair as playfair
import ngram_score as ns
import itertools

# imports scoring mechanism
fitness = ns.NgramScore('Texts/Frequencies/english_quadgrams.txt')

# loads cipher text from file and converts to uppercase
with open("texts/code_texts/playtest2.txt") as f:
    cipher_text = f.read()
cipher_text = re.sub('[^A-Z]','', cipher_text.upper())

# sets alphabet to generate initial random key
# note lack of 'J'
alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
# sets sequence to use for generating random numbers
# needed to avoid trying to swap same element
sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
            18, 19, 20, 21, 22, 23, 24]

# swap 2 letters at random, must be different
def swap_letters(key):
    x, y = random.sample(sequence, 2)
    key[y], key[x] = key[x], key[y]
    return key

# swap 2 rows at random, must be different
def swap_rows(key):
    x, y = random.sample(sequence[0:5], 2)
    x, y = (x * 5), (y * 5)
    key[y:y+5], key[x:x+5] = key[x:x+5], key[y:y+5]
    return key

# swap 2 columns at random, must be different
def swap_columns(key):
    x, y = random.sample(sequence[0:5], 2)
    key[y::5], key[x::5] = key[x::5], key[y::5]
    return key

# creates mirror of key along horizontal
def T_B_mirror(key):
    key[0:5], key[20:25] = key[20:25], key[0:5]
    key[5:10], key[15:20] = key[15:20], key[5:10]
    return key

# creates mirror of key along vertical
def L_R_mirror(key):
    key[0::5], key[4::5] = key[4::5], key[0::5]
    key[1::5], key[3::5] = key[3::5], key[1::5]
    return key

# creates mirror of key along top right to bottom left diagonal
def TR_BL_mirror(key):
    key[0:4], key[24:4:-5] = key[24:4:-5], key[0:4]
    key[5:8], key[23:8:-5] = key[23:8:-5], key[5:8]
    key[10:12], key[22:12:-5] = key[22:12:-5], key[10:12]
    key[15], key[21] = key[21], key[15]
    return key

# creates mirror of key along top left to bottom right diagonal
def TL_BR_mirror(key):
    key[1:5], key[5::5] = key[5::5], key[1:5]
    key[7:10], key[11::5] = key[11::5], key[7:10]
    key[13:15], key[17::5] = key[17::5], key[13:15]
    key[19], key[23] = key[23], key[19]
    return key

# sets initial temperature for simulated annealing

# sets inital score values
solutions = {}
results = []

for number in range(1, 21):
    print(number)
    T = 18
    stages = 0
# creates random initial key from alphabet
    best_key = random.sample(alphabet, 25)
    plain_text = playfair.Playfair(best_key).decipher(cipher_text)
    best_score = fitness.score(plain_text)

#    while T >= 0:
    while best_score < -2956 and stages < 15:
#    while stages < 50:
        stages += 1
        print(f"Stage: {stages}")
        current_key = [*best_key]
        plain_text = playfair.Playfair(current_key).decipher(cipher_text)
        current_score = fitness.score(plain_text)

        for i in range(9999):
            # performs random transformation of current key
            key = [*current_key]
            value = random.randint(0, 50)
            if value == 1:
                key = TL_BR_mirror(key)
            elif value == 2:
                key = TR_BL_mirror(key)
            elif value == 3:
                key = L_R_mirror(key)
            elif value == 4:
                key = T_B_mirror(key)
            elif value == 5 or value == 6:
                key = swap_columns(key)
            elif value == 7 or value == 8:
                key = swap_rows(key)
            else:
                key = swap_letters(key)

            plain_text = playfair.Playfair(key).decipher(cipher_text)
            candidate_score = fitness.score(plain_text)
            delta_score = candidate_score - current_score
            if delta_score >= 0 or random.random() < math.exp (delta_score / T):
                current_score, current_key = candidate_score, [*key]
                if current_score > best_score:
                    best_score, best_key = current_score, [*current_key]
                    flag = True
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
                            plain_text = myplayfair.Playfair(key).decipher(cipher_text)
                            candidate_score = fitness.score(plain_text)
                            if candidate_score > best_score:
                                best_score, best_key = candidate_score, [*key]
                                flag = True
                                break

                        # cycles through all row swaps sequentially
                        for x, y in iter2:
                            key = [*best_key]
                            key[y:y+5], key[x:x+5] = key[x:x+5], key[y:y+5]
                            plain_text = myplayfair.Playfair(key).decipher(cipher_text)
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

                    key = ''.join(best_key)
                    for i in range(0, 25, 5):
                        print(key[i:i+5])
                    plain_text = playfair.Playfair(key).decipher(cipher_text)
                    print(plain_text)
                    print(best_score)
                    print(T)

        T -= 0.2

    solutions[number] = best_key
    results.append((number, stages, best_score))

for key in solutions.values():
    key = ''.join(key)
    plain_text = playfair.Playfair(key).decipher(cipher_text)
    for i in range(0, 25, 5):
        print(key[i:i+5])
    print(plain_text)
    print()

for (number, stages, best_score) in results:
    if number < 10:
        print(f"0{number} = Stages: {stages} - Best Score: {best_score}")
    else:
        print(f"{number} = Stages: {stages} - Best Score: {best_score}")

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
