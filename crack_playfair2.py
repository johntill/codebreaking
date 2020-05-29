# import timeit

# code_to_test = """
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

def swap_all_elements(key):
    perms = itertools.combinations(range(25),2)
    for x, y in perms:
        key[x], key[y] = key[y], key[x]
        yield key

def swap_all_rows(key):
    perms = itertools.permutations(range(0,25,5),5)
    new_key = [None] * 25
    for perm in perms:
        for i in range(5):
            new_key[i*5:i*5+5] = key[perm[i]:perm[i]+5]
        yield new_key

def swap_all_columns(key):
    perms = itertools.permutations(range(5),5)
    new_key = [None] * 25
    for perm in perms:
        for i in range(5):
            new_key[i::5] = key[perm[i]::5]
        yield new_key

def swap_row_elements(key):
    for i in range(0,25,5):
        new_key = [*key]
        perms = itertools.permutations(range(5),5)
        for perm in perms:
            for j in range(5):
                new_key[i+j] = key[i+perm[j]]
            yield new_key

def swap_column_elements(key):
    for i in range(5):
        new_key = [*key]
        perms = itertools.permutations(range(0,25,5),5)       
        for perm in perms:
            for j in range(5):
                new_key[i+j*5] = key[i+perm[j]]
            yield new_key

def score_key(key):
    plain_text = playfair.Playfair(key).decipher(cipher_text)
    return fitness.score(plain_text), plain_text

def print_key(key):
    show_key = ''.join(key)
    for i in range(0, 25, 5):
        print(show_key[i:i+5])
    print()

solutions = {}
results = []

options = ([swap_all_elements, swap_all_rows, swap_all_columns,
            swap_row_elements, swap_column_elements])

for number in range(1, 10):
    print(f'Number: {number:02}')
    # sets initial temperature for simulated annealing
    T = 20000
    stages = 0
    best_stage = 0
    blank_stages = 0
# creates random initial key from alphabet
    best_key = random.sample(alphabet, 25)
    plain_text = playfair.Playfair(best_key).decipher(cipher_text)
    best_score = fitness.score(plain_text)

    while stages < 50:
        stages += 1
        print(f"Stage: {stages}, Blank Stages: {blank_stages}")
        current_key = [*best_key]
        plain_text = playfair.Playfair(current_key).decipher(cipher_text)
        current_score = fitness.score(plain_text)

        for option in options:
            for key in option(current_key):
                candidate_score, plain_text = score_key(key)
                delta_score = current_score - candidate_score
                if delta_score < 0 or math.exp(-delta_score / T) > 0.0085:
                    current_score, current_key = candidate_score, [*key]
                    #print(plain_text)
                if current_score > best_score:
                    best_score, best_key = current_score, [*current_key]
                    print_key(best_key)
                    print(plain_text)
                    print(best_score)
                    break

    solutions[number] = best_key
    results.append((number, best_stage, best_score))

for number, key in solutions.items():
    print(f'Solution: {number:02}')
    print_key(key)
    plain_text = playfair.Playfair(key).decipher(cipher_text)
    print(plain_text)
    print()

for (number, best_stage, best_score) in results:
    print(f"{number:02} = Best Stage: {best_stage:02} - Best Score: {best_score}")

# """

# elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
# print(elapsed_time)
