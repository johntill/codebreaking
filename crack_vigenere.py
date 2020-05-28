import timeit

code_to_test = """
import re
import code_vigenere as vigenere
import cipher_tools as tools
import ngram_score as ns

fitness = ns.NgramScore('texts/Frequencies/english_quadgrams.txt')

text = tools.import_cipher('texts/Code_texts/vigtest2.txt')

# Next step cycles though all keyword lengths of 2-30
# and calculates Index of Coincidence
# increase range if you think key word is > 15 characters
# the greater the range the more cipher text is needed
for n in range(2, 31):
    IC = 0
    for i in range(n):
        section = text[i::n]
        freqs = tools.frequency_analysis(section)
        IC += tools.calculate_IC(freqs, len(section))
    # if average IC for keylength scores highly enough
    # then end loop early and move to next step
    # value can be tuned if it's not giving correct key length
    # zero issues so far
    if (IC / n) > 0.06:
        key_len = n
        break

keyword = ['A'] * key_len
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
text_len = len(text)
best_score = -1000000

# runs IC scoring cycle to obtain initial key
# not really needed in practice
for i in range(key_len):
    best_IC = 0
    for letter in alphabet:
        keyword[i] = letter
        plain_text = vigenere.Vigenere(keyword).decipher(text)
        frequencies = tools.frequency_analysis(plain_text, alphabet)
        IC = tools.calculate_IC(frequencies, text_len)
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
            score = fitness.score(plain_text)
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
