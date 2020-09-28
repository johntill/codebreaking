# import timeit

# code_to_test = """
# Loads results of crack_enigma2.py from csv file then performs second
# half of decryption process to find correct plain text.

import re
from collections import defaultdict, Counter
from csv import reader

# Sets name of cipher text and results file to load.
cipher_file = 'texts/Code_texts/enigma_FHPQX.txt'
results_file = 'results/results_enigma_FHPQX.csv'

# Processes each row from csv file, sends it to assign_type and counts
# number of rows for each rotor setting in count_rotors dictionary.
def append_row(row):
    count_rotors[row[1]] += 1
    return assign_type(row)

# Breaks up the string from the csv file into IC score(float),
# rotors(Tuple) & settings(list) so they are in a usable form. Also adds
# new variable ringstellung with value [0, 0, 0].
def assign_type(row):
    IC = float(row[0])
    rotors = tuple(int(s) for s in re.findall(r'\d+', row[1]))
    settings = [int(s) for s in re.findall(r'\d+', row[2])]
    return rotors, IC, settings, [0, 0, 0]

# Loads results csv file and creates list containing top 20 results for
# each rotor setting.
with open(results_file) as f:
    data = reader(f)
    count_rotors = defaultdict(int)
    # results = [append_row(row) for row in data if count_rotors[row[1]] < 400]
    # results = [append_row(row) for row in data]

# For testing. Sets results to settings for correct solution to:
# medium2, FHPQX, cipherJG.
results = [((1, 2, 3), 0.04325625364253423, [11, 21, 9], [0, 0, 0]),
           ((3, 1, 2), 0.03694440788030363, [18, 10, 7], [0, 0, 0]),
           ((1, 0, 2), 0.04154852489147321, [1, 10, 5], [0, 0, 0])]

test_case = [(3, 1, 2), 0.04137598174718091, [18, 10, 7], [0, 0, 0]]

for result in results[:30]:
    print(result)

count = 0
for result in results:
    if result[0] == test_case[0]:
        count += 1
        if result[2] == test_case[2]:
            print(count, result)

with open(cipher_file) as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())
text_len = len(text)

letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,
           'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,
           'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
       'Q','R','S','T','U','V','W','X','Y','Z')

# Sets rotors (and their inverse for the way back) according to
# historical data. rotorkey[0] and invrotor[0] contain the values for
# Rotor I for example.
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

reflectorkey = ["EJMZALYXVBWFCRQUONTSPIKHGD",
                "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                "FVPJIAOYEDRZXWGCTKUQSBNMHL"]

reflector = 'B'
reflector = tuple(letters[i] for i in reflectorkey[letters[reflector]])

notch = ((16,), (4,), (21,), (9,), (25,))

steckers = []

def advance_rotor():
    if settings[1] in notch[rotors[1]]:
        settings[0] = (settings[0] + 1) % 26
        settings[1] = (settings[1] + 1) % 26
    if settings[2] in notch[rotors[2]]:
        settings[1] = (settings[1] + 1) % 26
    settings[2] = (settings[2] + 1) % 26

def apply_steckers(ch):
    for plug1, plug2 in steckers:
        if ch == plug1: return plug2
        if ch == plug2: return plug1
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
    # sourcery skip: comprehension-to-generator
    frequency_values = frequencies.values()
    f = sum(
        [v * (v - 1) for v in frequency_values]
    )
    return f / N

# Converts cipher text from letters to numbers.
text = [letters[i] for i in text]
# Sets value of N for use with calculate_IC as this won't vary.
N = text_len * (text_len - 1)

def filter_result(result, r):
    rotors, _, init_settings, ringstellung, highest_IC, _ = result
    count_rotors[rotors] += 1
    if r == 2:
        return rotors, highest_IC, init_settings, ringstellung
    return result

for r in (2, 1):
    print(len(results))
    ring_results = []
    for result in results:
        rotors, highest_IC, init_settings, ringstellung = result
        best_IC = highest_IC
        best_n = 0
        for n in range(26):
            settings = [*init_settings]
            ringstellung[r] = n
            settings[r] = (settings[r] + n) % 26
            plain = [encipher_char(ch) for ch in text]
            frequencies = Counter(plain)
            IC = calculate_IC(frequencies, N)
            if init_settings == [18, 10, 7] and r == 2 and n == 14:
                print(f'Correct = {count}, {result}')
            if init_settings == [18, 10, 21] and r == 1 and n == 19:
                print(f'Correct = {count}, {result}')
            if IC > best_IC:
                best_IC, best_n = IC, n
        init_settings[r] = (init_settings[r] + best_n) % 26
        ringstellung[r] = best_n
        individual_result = (rotors, highest_IC, init_settings, ringstellung,
                             best_IC, best_IC - highest_IC)
        ring_results.append(individual_result)
    ring_results = sorted(ring_results, reverse=True, key=lambda x: x[4])
    for result in ring_results[:30]:
        print(result)
    count = 0
    for result in ring_results:
        if result[0] == test_case[0]:
            count += 1
            if result[2][:r] == test_case[2][:r]:
                temp_r = (test_case[2][r] + result[3][r]) % 26
                temp = test_case[2]
                temp[r] = temp_r
                if temp == result[2]:
                    print(f'Highest = {count}, {result}')
                    test_case[2] = temp



    count_rotors = defaultdict(int)
    # results = ([filter_result(result, r) for result in ring_results
    #             if count_rotors[result[0]] < r*100])
    results = [filter_result(result, r) for result in ring_results]

print(len(results))

stecker_results = []

for result in results:
    rotors, _, init_settings, ringstellung, highest_IC, _ = result
    best_IC = highest_IC
    best_steckers = []
    for i in range(26):
        if i != 4:
            steckers = [(4, i)]
            settings = [*init_settings]
            plain = [encipher_char(ch) for ch in text]
            frequencies = Counter(plain)
            IC = calculate_IC(frequencies, N)
            if IC > best_IC:
                best_IC, best_steckers = IC, steckers
    result = (rotors, init_settings, ringstellung, highest_IC, best_steckers,
              best_IC, best_IC-highest_IC)
    stecker_results.append(result)

stecker_results = sorted(stecker_results, reverse=True, key=lambda x: x[5])

print()
for result in stecker_results[:30]:
    print(result)
print(len(stecker_results))

count = 0
for result in stecker_results:
    if result[0] == test_case[0]:
        count += 1
        if result[1] == test_case[2]:
            print(count, result)
    if result[1] == [18,3,21]:
        print(f'Correct = {count}, {result}')

rotors, init_settings, ringstellung, _, steckers, _, _ = stecker_results[0]
settings = [*init_settings]
plain = [encipher_char(ch) for ch in text]
plain = ''.join([arr[ch] for ch in plain])
frequencies = Counter(plain)
IC = calculate_IC(frequencies, N)

print(IC, rotors, init_settings, ringstellung, steckers)
print(plain)
# """

# elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
# print(elapsed_time)
