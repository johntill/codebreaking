from time import perf_counter
import cipher_tools as tools

start = perf_counter()

cipher_file = 'texts/Code_texts/Caesartest1.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'

text = tools.import_cipher(cipher_file)
text_len = len(text)

ngrams_ev = tools.expected_values(ev_file, text_len)
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decipher(text, alphabet, shift):
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)

def score_caesar(text, ngrams_ev, alphabet, shift):
    plaintext = decipher(text, alphabet, shift)
    freq = tools.frequency_analysis(plaintext, alphabet)
    chi_two = tools.chi_squared(freq, ngrams_ev)
    return chi_two, shift


scores = [
        score_caesar(text, ngrams_ev, alphabet, shift)
        for shift in range(len(alphabet))
        ]
        
best_shift = sorted(scores)[0][1]
plain_text = decipher(text, alphabet, best_shift)

end = perf_counter()
print(f'Best shift = {alphabet[best_shift]} ({best_shift})')
print(plain_text.lower())

print(f'{end-start}s')
