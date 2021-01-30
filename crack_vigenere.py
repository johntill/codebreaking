from time import perf_counter
import string
import cipher_tools as tools

start = perf_counter()

cipher_file = 'texts/Code_texts/vigtest2.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = tools.import_cipher(cipher_file)
text_len = len(text)

ngram_attributes = tools.create_ngram_attributes(ngram_file, text_len)

ngram_score_text = tools.ngram_score_text
frequency_analysis = tools.frequency_analysis
calculate_IC = tools.calculate_IC

alphabet = string.ascii_uppercase
letters = {ch: index for index, ch in enumerate(alphabet)}

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
else:
    print('No viable keylength found.')
    quit()

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

end = perf_counter()

print(f'Key = {keyword} - {key_len}')
print(plain_text.lower())

print(f'{end-start}s')