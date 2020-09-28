import timeit

code_to_test = """
# Program to perform first half of decryption of Enigma cipher text.
# This half iterates through all 26 x 26 x 26 x 60 rotor combinations
# and saves the results to a csv file in descending IC (Index of
# Coincidence) order.

import re
import itertools
from collections import Counter

# Name of file containing cipher.
cipher_file = 'texts/Code_texts/enigma_FHPQX.txt'
# Name of file that will contain results.
results_file = 'results/results_enigma_FHPQX.csv'

# Loads cipher text, removes any punctuation and converts to uppercase.
with open(cipher_file) as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())
text_len = len(text)

# Sets dictionary for translating letters in cipher text into numbers,
# this allows faster decryption. Will also be applied to rotors,
# reflectors etc. so that everything is in the same number form.
letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,
           'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,
           'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

# Sets rotors (and their inverse for the way back) according to
# historical data. rotorkey[0] and invrotor[0] contain the values
# for Rotor I for example.
rotorkey = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ",
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",
            "VZBRGITYUPSDNHLXAWMJQOFECK"]

invrotor = ["UWYGADFPVZBECKMTHXSLRINQOJ",
            "AJPCZWRLFBDKOTYUQGENHXMIVS",
            "TAGBPCSDQEUFVNZHYIXJWLRKOM",
            "HZWVARTNLGUPXQCEJMBSKDYOIF",
            "QCYLXWENFTZOSMVJUDKGIARPHB"]

# Translates rotorkey and invrotor from letters to numbers.
rotorkey = [[letters[i] for i in rotor] for rotor in rotorkey]
invrotor = [[letters[i] for i in rotor] for rotor in invrotor]

# Sets values for all 3 historical reflectors.
reflectorkey = ["EJMZALYXVBWFCRQUONTSPIKHGD",
                "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                "FVPJIAOYEDRZXWGCTKUQSBNMHL"]

# Sets reflector to 'B' as historically this was the one used.
# Can be changed to 'A' or 'C' if required. Then converts to numbers.
reflector = 'B'
reflector = tuple([letters[i] for i in reflectorkey[letters[reflector]]])

# Sets numerical values for the notches in the rotors. The notches
# caused the rotors to spin when encountered. The 8 notches correspond
# to the 8 rotors above, notch[0] corresponds to rotorkey[0] (or Rotor I).
notch = ((16,), (4,), (21,), (9,), (25,), (25,12), (25,12), (25,12))

# Function to simulate the spinning of the rotors. Advances the right-hand
# rotor (rotor[2]) every character and the other rotors when a notch
# is encountered. Note: This may cause rotors to spin more then once.
def advance_rotor():
    if settings[1] in notch[rotors[1]]:
        settings[0] = (settings[0] + 1) % 26
        settings[1] = (settings[1] + 1) % 26
    if settings[2] in notch[rotors[2]]:
        settings[1] = (settings[1] + 1) % 26
    settings[2] = (settings[2] + 1) % 26

def apply_rotor(ch, key, offset):
    ch = (ch + offset) % 26
    return (key[ch] - offset) % 26

# Simulates the passage of the character to be enciphered through the
# rotors. Starting with the fastest spinning, right-hand rotor first.
# The option to apply steckers has been removed as this is ignored at
# this stage of the process when trying to crack the cipher.
def encipher_char(ch):
    advance_rotor()
    for i in (2, 1, 0):
        ch = apply_rotor(ch, rotorkey[rotors[i]], settings[i])
    ch = reflector[ch]
    for i in (0, 1, 2):
        ch = apply_rotor(ch, invrotor[rotors[i]], settings[i])
    return ch

def calculate_IC(frequencies, N):
    frequency_values = frequencies.values()
    f = sum(
        [v * (v - 1) for v in frequency_values]
    )
    return f / N

# Converts cipher text from letters to numbers.
text = [letters[i] for i in text]
# Sets value of N for use with calculate_IC as this won't vary.
N = text_len * (text_len - 1)

results = []
poss_rotors = itertools.permutations(range(5), 3)

for rotors in poss_rotors:
    print(rotors)
    poss_settings = itertools.product(range(26), repeat=3)
    for initsettings in poss_settings:
        settings = [*initsettings]
        plain = [encipher_char(ch) for ch in text]
        frequencies = Counter(plain)
        IC = calculate_IC(frequencies, N)
        results.append((IC, rotors, initsettings))

# Sorts results in order of Index of Coincidence score, highest to lowest.
results = sorted(results, reverse=True)

# Saves results to results file
def save_results(results_file, results):
    from csv import writer
    with open(results_file, 'w', newline='') as f:
        wr = writer(f)
        wr.writerows(results)

# Optional line to save results list to csv file
save_results(results_file, results)

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)
