import timeit

code_to_test = """

import re

cipher_file = 'texts/Code_texts/Caesartest1.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'

def import_cipher(filename):
    # loads cipher text from a file
    with open(filename, 'r', encoding='utf8', errors='ignore') as f:
        text = f.read()
    # Removes punctuation & whitespace, converts to all UPPERCASE
    return re.sub('[^A-Z]','', text.upper())

def frequency_analysis(text, alphabet=None):
    if not alphabet: alphabet = set(text)
    text_count = text.count
    return {char : text_count(char) for char in alphabet}

def calculate_IC(frequencies, text_len):
    # sourcery skip: comprehension-to-generator
    frequency_values = frequencies.values()
    sum_freqs = sum(
        [letter_freq * (letter_freq - 1) for letter_freq in frequency_values]
    )
    return sum_freqs / (text_len * (text_len - 1))

def calculate_IC2(frequencies, text_constant):
    # sourcery skip: comprehension-to-generator
    frequency_values = frequencies.values()
    freqs = [letter_freq * (letter_freq - 1) for letter_freq in frequency_values]
    return sum(freqs) / text_constant

text = import_cipher(cipher_file)
text_len = len(text)

key_len = 10
full_rows, num_long_col = divmod(text_len, key_len)

half_len = int(text_len/2)
#half_len = 10
# column_a = text[:half_len]
# column_b = text[half_len:]

column_a = text[:5]
column_b = text[5:11]

# print(text)
print(column_a)
print(column_b)



for _ in range(1):
    for char_a, char_b in zip(column_b, column_a):
        x = char_a + char_b
        #x = char_b + char_a
        print(x)



# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# freqs = frequency_analysis(text, alphabet)
# text_constant = text_len * (text_len - 1)
# for _ in range(350_000):
#     IC = calculate_IC(freqs, text_len)

#print(text)
#print(IC)

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)