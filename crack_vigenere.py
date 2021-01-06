import timeit

code_to_test = """

import cipher_tools as ct

cipher_file = 'texts/Code_texts/vigtest1.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = ct.import_cipher(cipher_file)
text_len = len(text)

ngram_attributes = ct.create_ngram_attributes(ngram_file, text_len)

ngram_score_text = ct.ngram_score_text
frequency_analysis = ct.frequency_analysis
calculate_IC = ct.calculate_IC

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,
           'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,'S':18,'T':19,'U':20,
           'V':21,'W':22,'X':23,'Y':24,'Z':25}

# Cycles though all keyword lengths of 2-30 and calculates Index of Coincidence.
# Increase range if you think key word is > 15 characters, the greater the
# range the more cipher text is needed.
for possible_key_len in range(2, 31):
    IC = 0
    for i in range(possible_key_len):
        section = text[i::possible_key_len]
        freqs = frequency_analysis(section, alphabet)
        IC += calculate_IC(freqs, len(section))
    # If average IC for keylength scores highly enough then end loop
    # early and move to next step. Value can be tuned if it's not giving
    # correct key length.
    if (IC / possible_key_len) > 0.06:
        key_len = possible_key_len
        break

def decipher(text, key):
    trans_text = [None] * text_len
    for i, ch in enumerate(key):
        section = text[i::key_len]
        shifted_alphabet = alphabet[letters[ch]:] + alphabet[:letters[ch]]
        table = str.maketrans(shifted_alphabet, alphabet)
        trans_text[i::key_len] = section.translate(table)
    return ''.join(trans_text)

keyword = ['A'] * key_len
best_score = -1000000

# runs quadgram scoring cycle twice
# can be increased if correct key not found
for _ in range(2):
    for i in range(key_len):
        for letter in alphabet:
            keyword[i] = letter
            plain_text = decipher(text, keyword)
            score = ngram_score_text(plain_text, ngram_attributes)
            if score >= best_score:
                best_score, best_letter = score, letter
        keyword[i] = best_letter

keyword = ''.join(keyword)
plain_text = decipher(text, keyword)
print(f"Key = {keyword}")
print(plain_text.lower())
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
