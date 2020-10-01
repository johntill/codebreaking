import re
from collections import defaultdict
from math import log10


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
    expected_N = text_len / N
    for key, value in ngrams_ev.items():
        ngrams_ev[key] = value * expected_N
    return ngrams_ev

# Create dictionary of characters and character counts in a text.
def frequency_analysis(text, alphabet=None):
    if not alphabet: alphabet = set(text)
    text_count = text.count
    return {char : text_count(char) for char in alphabet}

# Calculates the IC (Index of Coincidence) of a text.
def calculate_IC(frequencies, text_len):
    # sourcery skip: comprehension-to-generator
    frequency_values = frequencies.values()
    sum_freqs = sum(
        [letter_freq * (letter_freq - 1) for letter_freq in frequency_values]
    )
    return sum_freqs / (text_len * (text_len - 1))

# Calculates the Chi Squared score of a text.
def chi_squared(frequencies, ngrams_ev):
    frequency_items = frequencies.items()
    chi_two = 0
    for char, frequency in frequency_items:
        expected_frequency = ngrams_ev[char]
        chi_two += (frequency - expected_frequency) ** 2 / expected_frequency
    return chi_two

# Create dictionary of Ngram frequencies in a text.
def ngram_freq_counter(text, ngram_size, step=1):
    n_grams = defaultdict(int)
    for i in range(0, len(text) - ngram_size + 1, step):
        n_grams[text[i:i+ngram_size]] += 1
    return n_grams

# Create array and attributes for Ngram scoring.
def ngram_create_scoring_attributes(ngram_file, text_len):
    ngrams = {}
    with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
        for line in f:
            ngram, _, count = line.partition(' ')
            ngrams[ngram] = float(count)
    count_total = sum(ngrams.values())
    floor = log10(0.01 / count_total)
    ngram_len = len(ngram)
    scoring_range = range(text_len - ngram_len + 1)
    for ngram, count in ngrams.items():
        ngrams[ngram] = log10(count / count_total)
    return ngrams, ngram_len, floor, scoring_range

# Calculate Ngram score of text using ngram array and attriibutes.
def ngram_score_text(text, attributes):
    ngrams, ngram_len, floor, scoring_range = attributes 
    score = 0
    for i in scoring_range:
        try:
            score += ngrams[text[i:i+ngram_len]]
        except:
            score += floor
    return score