import timeit

code_to_test = """
# Program to perform first half of decryption of Enigma cipher text.
# This half iterates through all 26 x 26 x 26 x 60 rotor combinations
# and saves the results to a csv file in descending IC (index of Coincidence) order.

import re
import itertools

# Name of file containing cipher.
cipher_file = 'texts/Code_texts/enigma_medium2.txt'
# Name of file that will contain results.
results_file = 'results/results_enigma_medium2.csv'

# Loads cipher text, removes any punctuation and converts to uppercase
with open(cipher_file) as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())
text_len = len(text)

letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
   'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
   'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}



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

def encipher_char(ch):
    advance_rotor()
    for i in (2, 1, 0):
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, rotorkey[rotors[i]], offset)
    ch = reflector[ch]
    for i in (0, 1, 2):
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, invrotor[rotors[i]], offset)
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

ringstellung = (0, 0, 0)
results = []
poss_rotors = itertools.permutations(range(5), 3)

for rotors in poss_rotors:
    print(rotors)
    poss_settings = itertools.product(range(26), repeat=3)
    for settings in poss_settings:
        initsettings = tuple(settings)
        settings = [*initsettings]
        plain = [encipher_char(ch) for ch in text]
        frequencies = frequency_analysis(plain)
        IC = calculate_IC(frequencies, N)
        results.append((IC, rotors, initsettings))

# Sorts results in IC order, largest to smallest
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
