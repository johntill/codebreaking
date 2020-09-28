import timeit

code_to_test = """
import re

import cipher_tools as ct
import code_vigenere as vigenere

cipher_file = 'texts/Code_texts/vigtest2.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = ct.import_cipher(cipher_file)
text_len = len(text)

ngram_create_scoring_attributes = ct.ngram_create_scoring_attributes
ngram_score_text = ct.ngram_score_text
ngram_attributes = ngram_create_scoring_attributes(ngram_file, text_len)

frequency_analysis = ct.frequency_analysis
calculate_IC = ct.calculate_IC

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Cycles though all keyword lengths of 2-30 and calculates Index of Coincidence.
# Increase range if you think key word is > 15 characters, the greater the
# range the more cipher text is needed.
for n in range(2, 31):
    IC = 0
    for i in range(n):
        section = text[i::n]
        freqs = frequency_analysis(section, alphabet)
        IC += calculate_IC(freqs, len(section))
    # If average IC for keylength scores highly enough then end loop
    # early and move to next step. Value can be tuned if it's not giving
    # correct key length.
    if (IC / n) > 0.06:
        key_len = n
        break

keyword = ['A'] * key_len
best_score = -1000000

# runs IC scoring cycle to obtain initial key
# not really needed in practice
for i in range(key_len):
    best_IC = 0
    for letter in alphabet:
        keyword[i] = letter
        plain_text = vigenere.Vigenere(keyword).decipher(text)
        frequencies = frequency_analysis(plain_text, alphabet)
        IC = calculate_IC(frequencies, text_len)
        if IC >= best_IC:
            best_IC, best_letter = IC, letter
    keyword[i] = best_letter

# runs quadgram scoring cycle twice
# can be increased if correct key not found
for _ in range(2):
    for i in range(key_len):
        for letter in alphabet:
            keyword[i] = letter
            plain_text = vigenere.Vigenere(keyword).decipher(text)
            score = ngram_score_text(plain_text, ngram_attributes)
            if score >= best_score:
                best_score, best_letter = score, letter
        keyword[i] = best_letter

keyword = ''.join(keyword)
plain_text = vigenere.Vigenere(keyword).decipher(text)
print(f"Key = {keyword}")
print(plain_text.lower())
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
