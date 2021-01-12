# import timeit

# code_to_test = """
import itertools
import re
import random
import time
import cipher_tools as tools
from collections import Counter

cipher_file = 'texts/Code_texts/subtest4.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

cipher_text = tools.import_cipher(cipher_file)
text_len = len(cipher_text)
#print(cipher_text)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_sequence = [*range(len(alphabet))]

def letter_expected_values(ev_file, alphabet):
    ngrams_ev = {}
    for line in open(ev_file, 'r'):
        key, _, count = line.partition(' ')
        if key in alphabet:
            ngrams_ev[key] = float(count)
    for char in alphabet:
        if char not in ngrams_ev:
            ngrams_ev[char] = 0
    count_total = sum(ngrams_ev.values())
    for ngram, score in ngrams_ev.items():
        ngrams_ev[ngram] = score / count_total
    return ngrams_ev

def create_weighted_list(ev_list, ngrams_ev):
    weighted_ev_list = []
    for letter, frequency in ngrams_ev.items():
        index = alphabet.index(letter)
        weighted_ev_list.extend([index] * int(10_000 * frequency))
    return weighted_ev_list

def set_key(frequencies, ev_list, alphabet):
    key_list = sorted(frequencies, key=frequencies.get, reverse=True)   
    key_list = ''.join(key_list)
    table = str.maketrans(ev_list, key_list)
    return alphabet.translate(table)

def decrypt(cipher_text, key):
    key = ''.join(key)
    table = str.maketrans(key, alphabet)
    return cipher_text.translate(table)

# swap 2 letters at random, must be different
def swap_letters(old_key, letter_choices):
    while True:
        x, y = random.sample(letter_choices, 2)
        if x != y:
            key = [*old_key]
            key[y], key[x] = key[x], key[y]
            return key

attributes = tools.create_ngram_attributes(ngram_file, text_len)
score_text = tools.ngram_score_text
ngrams_ev = letter_expected_values(ev_file, alphabet)
#print(ngrams_ev)
ev_list = ''.join(sorted(ngrams_ev, key=ngrams_ev.get, reverse=True))
#print(f'Expected - {ev_list}')
weighted_ev_list = create_weighted_list(ev_list, ngrams_ev)
#print(weighted_ev_list)
frequencies = tools.frequency_analysis(cipher_text, alphabet)
#print(frequencies)
best_score = -10_000_000
low_letters = ev_list[-14:]
indices = [alphabet.index(letter) for letter in low_letters]

# key_list = sorted(frequencies, key=frequencies.get, reverse=True)   
# key_list = ''.join(key_list)
# print(f'Midway   - {key_list}')
# current_key = set_key(frequencies, ev_list, alphabet)
# print(f'Current  - {current_key}')

cipher_scores = ({'texts/Code_texts/subtest1.txt': -355,
                  'texts/Code_texts/subtest2.txt': -522,
                  'texts/Code_texts/subtest3.txt': -1103,
                  'texts/Code_texts/subtest4.txt': -1031,
                  'texts/Code_texts/subtest5.txt': -1787,
                  'texts/Code_texts/subtest6.txt': -2308,
                  'texts/Code_texts/subtest7.txt': -3282})

target_score = cipher_scores[cipher_file]
attempts = 1000
for iterations in range(1000, 5500, 500):
    success = 0
    help_count = 0
    count_list = []
    successful_counts = []
    no_improvement_list = []
    start = time.perf_counter()
    for _ in range(attempts):
        #current_key = [*alphabet]
        #random.shuffle(current_key)
        current_key = set_key(frequencies, ev_list, alphabet)
        plain_text = decrypt(cipher_text, current_key)
        current_score = score_text(plain_text, attributes)
        count = 0
        no_improvement = 0
        #for i in range(iterations):
        while no_improvement < iterations:
            count += 1
            key = swap_letters(current_key, alphabet_sequence)
            #key = swap_letters(current_key, weighted_ev_list)
            # if i < iterations // 2:
            #     key = swap_letters(current_key, weighted_ev_list)
            # else:
            #     key = swap_letters(current_key, alphabet_sequence)
            plain_text = decrypt(cipher_text, key)
            candidate_score = score_text(plain_text, attributes)
            if candidate_score > current_score:
                current_score, current_key = candidate_score, [*key]
                no_improvement_list.append(no_improvement)
                no_improvement = 0
                if current_score > target_score:
                    successful_counts.append(count)
            else:
                no_improvement += 1
            
        count_list.append(count)
        plain_text = decrypt(cipher_text, current_key)
        current_score = score_text(plain_text, attributes)
        #print(plain_text)
        #print(current_score)
        iter = itertools.combinations(indices, 2)
        helped = False
        for x, y in iter:
            key = [*current_key]
            key[y], key[x] = key[x], key[y]
            plain_text = decrypt(cipher_text, key)
            candidate_score = score_text(plain_text, attributes)
            if candidate_score > current_score:
                helped = True
                #print(plain_text)
                current_score, current_key = candidate_score, [*key]
                #print(candidate_score)

        if current_score > best_score:
            best_score, best_key = current_score, [*current_key]

        if current_score > target_score:
            success += 1
            help_count += helped
            #plain_text = decrypt(cipher_text, current_key)
            #print(plain_text)
            #print(current_score)

    end = time.perf_counter()

    # best_key = ''.join(best_key)
    # print(f'Best key - {best_key}')
    # plain_text = decrypt(cipher_text, best_key)
    # print(plain_text)
    # print(best_score)

    print(f'ITERATIONS = {iterations}')
    print(f'Successes = {success} / {attempts} = {success/attempts*100}%')
    print(f'Help rate = {help_count} / {attempts}')
    print(f'Average Count = {sum(count_list)/attempts}')
    print(f'Max count = {max(count_list)}')
    print(f'Min count = {min(count_list)}')
    if not successful_counts:
        successful_counts.append(0)
    av_count = sum(successful_counts) / len(successful_counts)
    print(f'Average successful count = {av_count}')
    print(f'Max successful count = {max(successful_counts)}')
    print(f'Min successful count = {min(successful_counts)}')
    print(f'Max no improvement = {max(no_improvement_list)}')
    # ni = Counter(no_improvement_list)
    # ni_keys = sorted(ni, reverse=True)
    # for count in ni_keys[:20]:
    #     print(count)
    time_taken = end - start
    print(f'{time_taken:.2f}s - {time_taken/attempts:.2f}s')
    print()
# """

# elapsed_time = timeit.timeit(code_to_test, number = 1)#/1
# print(elapsed_time)
