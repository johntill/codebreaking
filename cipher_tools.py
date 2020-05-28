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
    f = 0
    N = text_len * (text_len - 1)
    for v in frequencies.values():
        f += v * (v - 1)
    return f / N

# calculates the Chi Squared score of a text
def chi_squared(frequencies, ngrams_ev):
    chi_two = 0
    for char, value in frequencies.items():
        E = ngrams_ev[char]
        chi_two += ((value - E) ** 2) / E
    return chi_two

def ngram_freq_counter(text, ngram_size, step=1):
    n_gram = defaultdict(int)
    for i in range(0, len(text)-ngram_size+1, step):
        n_gram[text[i:i+ngram_size]] += 1
    return n_gram