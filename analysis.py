import cipher_tools as tools
import code_caesar as caesar
from collections import defaultdict, Counter

# Loads a cipher text and analyses it to help determine the cipher
# used to encrypt it.
# Also offers to decrypt a Caesar cipher or test whether the cipher text
# has a periodic IC which is the fingerprint of certain ciphers.


# bi, tri and quad_gram frequencies use different methods
# to create the frequencies dictionary and count
# defaultdict is fastest, followed by Counter and then get
def bi_gram_freq(text, text_len):
    n_gram = {}
    for c in range(0, text_len-1, 2):
        n_gram[text[c:c+2]] = n_gram.get(text[c:c+2], 0) + 1
    return n_gram

def tri_gram_freq(text, text_len):
    n_gram = Counter()
    for c in range(0, text_len-2, 1):
        n_gram[text[c:c+3]] += 1
    return n_gram

def quad_gram_freq(text, text_len):
    n_gram = defaultdict(int)
    for c in range(0, text_len-3, 1):
        n_gram[text[c:c+4]] += 1
    return n_gram

def print_freq(frequencies):
    for char, value in sorted(frequencies.items()):
        print(char, value)

def print_freq_inc_nulls(frequencies, alphabet):
    for char in alphabet:
        if char in frequencies:
            print(char, frequencies[char])
        else:
            print(char, 0)

# function that tries all 26 different possibilities of the Caesar cipher
# then uses the Chi squared score of each to display the correct translation
def score_caesar(text, ngrams_ev, shift):
    plaintext = caesar.Caesar(shift).decipher(text)
    freq = tools.frequency_analysis(plaintext)
    chi_two = tools.chi_squared(freq, ngrams_ev)    
    print(f'{shift:02} : {plaintext[:15]} : {chi_two:.4f}')
    return (chi_two, shift)

# Calculates average IC for all keylengths 2-31
# will reveal keylength for repeating polyalphabetical ciphers
# e.g. Vigenere
def periodic_IC(text):
    key_scores = []
    for key_len in range(2, 31):
        IC = 0
        spike = ""
        for i in range(key_len):
            section = text[i::key_len]
            freqs = tools.frequency_analysis(section)
            IC += tools.calculate_IC(freqs, len(section))
        if (av_IC := IC / key_len) >= 0.06:
            key_scores.append(key_len)
            spike = "***"
        print(f"n = {key_len:02}, Average IC = {av_IC:.4f} {spike}")
    return key_scores

def main():
    text = tools.import_cipher('Texts/Code_texts/vigtest2.txt')
    text_len = len(text)
    ngrams_ev = tools.expected_values('Texts/Frequencies/english_monograms.txt', text_len)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    print(f"\nText length: {text_len}")

    frequencies = tools.frequency_analysis(text)
    freq_len = len(frequencies)
    print(f"Number of unique letters: {freq_len}")

    chi_two = tools.chi_squared(frequencies, ngrams_ev)
    print(f"Chi squared score: {chi_two}\n")

    IC = tools.calculate_IC(frequencies, text_len)
    print(f"IC value: {IC}")

    bi_gram = bi_gram_freq(text, text_len)
    bi_IC = tools.calculate_IC(bi_gram, text_len)
    print(f"Bigram IC value: {bi_IC}")

    tri_gram = tri_gram_freq(text, text_len)
    tri_IC = tools.calculate_IC(tri_gram, text_len)
    print(f"Trigram IC value: {tri_IC}")

    quad_gram = quad_gram_freq(text, text_len)
    quad_IC = tools.calculate_IC(quad_gram, text_len)
    print(f"Quadgram IC value: {quad_IC}")

    if freq_len == 2:
        print("The cipher is likely Baconian")
    elif freq_len < 10 and bi_IC > 0.06:
        print("The cipher is likely a polybius square cipher")
        print("and should be solvable via frequency analysis")
    elif freq_len < 10 and bi_IC < 0.06:
        print("The cipher is likely an ADFGX, ADFGVX or a variant")
    elif freq_len > 26:
        print("The cipher is likely either a homophonic substituion cipher")
        print("or is using codewords as well as substitution")
    elif freq_len < 26 and 'J' not in frequencies and IC < 0.06 \
        and text_len % 2 == 0:
        print("This may be a Playfair cipher or similar variant")

    ask = input("\nDo you want to show letter frequencies? (y/n): ")
    if ask == 'y':
        ask = input("Do you want to include absent letters? (y/n): ")
        print()
        if ask == 'y':
            print_freq_inc_nulls(frequencies, alphabet)
        else:
            print_freq(frequencies)

    ask = input("\nDo you want to show bigram frequencies? (y/n): ")
    if ask == 'y':
        print_freq(bi_gram)
        print(f"Number of bigrams = {len(bi_gram)}")

    ask = input("\nDo you want to show trigram & quadgram frequencies? (y/n): ")
    if ask == 'y':
        print_freq(tri_gram)
        print(f"Number of trigrams = {len(tri_gram)}")
        print_freq(quad_gram)
        print(f"Number of quadgrams = {len(quad_gram)}")

    # Offers to decrypt Caesar shift cipher if IC above 0.06
    # as too simple to warrant own program
    if IC >= 0.06:
        ask = input("\nAttempt Caesar Shift decryption? (y/n): ")
        if ask == 'y':
            print()
            scores = [score_caesar(text, ngrams_ev, shift) for shift in range(26)]
            best_shift = sorted(scores)[0][1]
            plain_text = caesar.Caesar(best_shift).decipher(text)
            print(f"\nOriginal shift = {alphabet[best_shift]} ({best_shift})\n")
            print(plain_text.lower())
            print()

    # runs periodic_IC function if required
    if IC < 0.06:
        ask = input("\nCheck for periodic IC? (y/n): ")
        if ask == "y":
            print()
            key_scores = periodic_IC(text)
            print(f"\nLikely key length is {key_scores[0]}")
            print(f"(Other spikes found at {key_scores[1:]})\n")

if __name__ == "__main__":
    main()