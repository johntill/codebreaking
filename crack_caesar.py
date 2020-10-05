import timeit

code_to_test = """

import cipher_tools as ct

cipher_file = 'texts/Code_texts/Caesartest1.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'

def decipher(text, alphabet, shift):
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)

def score_caesar(text, ngrams_ev, alphabet, shift):
    plaintext = decipher(text, alphabet, shift)
    freq = ct.frequency_analysis(plaintext, alphabet)
    chi_two = ct.chi_squared(freq, ngrams_ev)
    return chi_two, shift

text = ct.import_cipher(cipher_file)
text_len = len(text)

ngrams_ev = ct.expected_values(ev_file, text_len)
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

scores = [score_caesar(text, ngrams_ev, alphabet, shift) for shift in range(26)]
best_shift = sorted(scores)[0][1]
plain_text = decipher(text, alphabet, best_shift)
print(alphabet[best_shift], best_shift)
print(plain_text.lower())

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)