import re
from collections import defaultdict

def import_cipher(filename):
    # loads cipher text from a file
    with open(filename, 'r', encoding='utf8', errors='ignore') as f:
        text = f.read()
    # Removes punctuation & whitespace, converts to all UPPERCASE
    return re.sub('[^A-Z]','', text.upper())

def expected_values(filename, text_len=100):
    # Loads standard expected frequencies from chosen file
    # and adjusts for length of text. If no text length
    # is given then converts to a percentage.
    ngrams_ev = {}
    for line in open(filename, 'r', encoding='utf8', errors='ignore'):
        key, _, count = line.partition(' ')
        ngrams_ev[key] = float(count)
    N = sum(ngrams_ev.values())
    for key in ngrams_ev.keys():
        ngrams_ev[key] = (ngrams_ev[key] / N) * text_len
    return ngrams_ev

def frequency_analysis(text, alphabet=None):
    if not alphabet: alphabet = set(text)
    return {char : text.count(char) for char in alphabet}

# calculates the IC (Index of Coincidence) of a text
def calculate_IC(frequencies, text_len):
    sum_freqs = 0
    for letter_freq in frequencies.values():
        sum_freqs += letter_freq * (letter_freq - 1)
    return sum_freqs / (text_len * (text_len - 1))

# calculates the Chi Squared score of a text
def chi_squared(frequencies, ngrams_ev):
    chi_two = 0
    for char, frequency in frequencies.items():
        expected_frequency = ngrams_ev[char]
        chi_two += (frequency - expected_frequency) ** 2 / expected_frequency
    return chi_two

def ngram_freq_counter(text, ngram_size, step=1):
    n_grams = defaultdict(int)
    for i in range(0, len(text) - ngram_size + 1, step):
        n_grams[text[i:i+ngram_size]] += 1
    return n_grams