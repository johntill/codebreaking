import timeit

code_to_test = """
# Loads results of crack_enigma2.py from csv file then performs second half of
# decryption process to find correct plain text

import csv
import re
from collections import defaultdict, Counter

# sets name of cipher text and results file (from crack_enigma2.py) to be loaded
cipher_file = 'texts/Code_texts/enigma_medium2.txt'
results_file = 'results/results_enigma_medium2.csv'

# Processes each row from csv file, sends it to assign_type and counts number
# of rows from each rotor setting in count_rotors default dictionary.
def append_row(row):
    count_rotors[row[1]] += 1
    return assign_type(row)

# Breaks up the string from the csv file into IC score(float), rotors(Tuple)
# & settings(list) so they are in a usable form.
def assign_type(row):
    IC = float(row[0])
    rotors = tuple([int(s) for s in re.findall(r'\d+', row[1])])
    settings = [int(s) for s in re.findall(r'\d+', row[2])]
    return IC, rotors, settings

# Loads results csv file and creates list containing top 20 results for each rotor setting.
with open(results_file) as f:
    data = csv.reader(f)
    count_rotors = defaultdict(int)
    results = [append_row(row) for row in data if count_rotors[row[1]] < 20]

for result in results[:30]:
    print(result)

import itertools

with open(cipher_file) as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())
text_len = len(text)

letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
   'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
   'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
       'P','Q','R','S','T','U','V','W','X','Y','Z')

rotorkey = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ",
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",
            "VZBRGITYUPSDNHLXAWMJQOFECK",
            "JPGVOUMFYQBENHZRDKASXLICTW",
            "NZJHGRCXMYSWBOUFAIVLPEKQDT",
            "FKQHTLXOCBJSPDZRAMEWNIUYGV"]
invrotor = ["UWYGADFPVZBECKMTHXSLRINQOJ",
            "AJPCZWRLFBDKOTYUQGENHXMIVS",
            "TAGBPCSDQEUFVNZHYIXJWLRKOM",
            "HZWVARTNLGUPXQCEJMBSKDYOIF",
            "QCYLXWENFTZOSMVJUDKGIARPHB",
            "SKXQLHCNWARVGMEBJPTYFDZUIO",
            "QMGYVPEDRCWTIANUXFKZOSLHJB",
            "QJINSAYDVKBFRUHMCPLEWZTGXO"]

for r in range(len(rotorkey)):
    rotorkey[r] = [letters[i] for i in rotorkey[r]]
    invrotor[r] = [letters[i] for i in invrotor[r]]

reflectorkey = ["EJMZALYXVBWFCRQUONTSPIKHGD",
                "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                "FVPJIAOYEDRZXWGCTKUQSBNMHL"]

reflector = 'B'
reflector = tuple([letters[i] for i in reflectorkey[letters[reflector]]])

notch = ((16,),(4,),(21,),(9,),(25,),(25,12),(25,12),(25,12))

steckers = []

def advance_rotor():
    if settings[1] in notch[rotors[1]]:
        settings[0] = (settings[0] + 1) % 26
        settings[1] = (settings[1] + 1) % 26
    if settings[2] in notch[rotors[2]]:
        settings[1] = (settings[1] + 1) % 26
    settings[2] = (settings[2] + 1) % 26

def apply_steckers(ch):
    for i in steckers:
        if ch == i[0]:
            return i[1]
        if ch == i[1]:
            return i[0]
    return ch

def apply_rotor(ch, key, offset):
    ch = (ch + offset) % 26
    return (key[ch] - offset) % 26

def encipher_char(ch):
    advance_rotor()
    if steckers:
        ch = apply_steckers(ch)
    for i in (2, 1, 0):
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, rotorkey[rotors[i]], offset)
    ch = reflector[ch]
    for i in (0, 1, 2):
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, invrotor[rotors[i]], offset)
    if steckers:
        ch = apply_steckers(ch)
    return ch

def calculate_IC(frequencies, N):
    f = 0
    for v in frequencies.values():
        f += v * (v - 1)
    return f / N

def frequency_analysis(text):
    return {char : text.count(char) for char in set(text)}

text = [letters[i] for i in text]
N = text_len * (text_len - 1)

results2 = []
for result in results:
    best_IC, rotors, init_settings = result
    init_settings = list(init_settings)
    ringstellung = [0, 0, 0]
    highest_IC = 0
    for r in (2, 1):
        for n in range(26):
            settings = [*init_settings]
            ringstellung[r] = n
            settings[r] = (settings[r] + n) % 26
            plain = [encipher_char(ch) for ch in text]
            frequencies = Counter(plain)
            IC = calculate_IC(frequencies, N)
            if IC > highest_IC:
                highest_IC = IC
                highest_n = n
        init_settings[r] = (init_settings[r] + highest_n) % 26
        ringstellung[r] = highest_n
    individual_result = (rotors, best_IC, init_settings, ringstellung, highest_IC, highest_IC - best_IC)
    # print(individual_result)
    results2.append(individual_result)

results2 = sorted(results2, reverse=True, key=lambda x: x[4])
print()
for result in results2[:30]:
    print(result)

stecker_result = []
best_steckers = []
for result in results2:
    rotors, _, init_settings, ringstellung, best_IC, _ = result
    highest_IC = best_IC
    for i in range(26):
        if i != 4:
            steckers = [(4, i)]
            settings = [*init_settings]
            plain = [encipher_char(ch) for ch in text]
            frequencies = Counter(plain)
            IC = calculate_IC(frequencies, N)
            if IC > best_IC:
                best_IC = IC
                best_steckers = steckers
    result = (rotors, init_settings, ringstellung, highest_IC, best_steckers, best_IC, best_IC-highest_IC)
    stecker_result.append(result)

stecker_result = sorted(stecker_result, reverse=True, key=lambda x: x[5])

print()
for result in stecker_result[:30]:
    print(result)

rotors, init_settings, ringstellung, _, steckers, _, _ = stecker_result[0]
settings = [*init_settings]
plain = [encipher_char(ch) for ch in text]
plain = [arr[ch] for ch in plain]
frequencies = Counter(plain)
IC = calculate_IC(frequencies, N)

print(IC, rotors, init_settings, ringstellung, steckers)
plain = ''.join(plain)
print(plain)
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
