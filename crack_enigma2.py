import timeit

code_to_test = """
import re
import itertools

with open("enigmacipher2.txt") as f:
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
    #ch = apply_steckers(ch)
    for i in (2, 1, 0):
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, rotorkey[rotors[i]], offset)
    ch = reflector[ch]
    for i in (0, 1, 2):
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, invrotor[rotors[i]], offset)
    #ch = apply_steckers(ch)
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
    poss_settings = itertools.product(range(26), repeat=3)
    for settings in poss_settings:
        initsettings = tuple(settings)
        settings = [*initsettings]
        plain = [encipher_char(ch) for ch in text]
        frequencies = frequency_analysis(plain)
        IC = calculate_IC(frequencies, N)
        results.append((IC, rotors, initsettings))

results = sorted(results, reverse = True)

check_set = set()
new_results = []

for result in results:
    if result[1] not in check_set:
        check_set.add(result[1])
        new_results.append(result)
        if len(check_set) == 6:
            break

print(new_results)

best_IC, rotors, init_settings = new_results[0]
ringstellung = [0, 0, 0]
init_settings = list(init_settings)
best_n = 0

for r in (2, 1):
    for n in range(26):
        settings = [*init_settings]
        ringstellung[r] = n
        settings[r] = (settings[r] + n) % 26
        plain = [encipher_char(ch) for ch in text]
        frequencies = frequency_analysis(plain)
        IC = calculate_IC(frequencies, N)
        if IC > best_IC:
            best_IC = IC
            best_n = n
    init_settings[r] = (init_settings[r] + best_n) % 26
    ringstellung[r] = best_n

print(init_settings, ringstellung)

settings = init_settings
plain = [arr[ch] for ch in plain]
plain = ''.join(plain)
print(plain)

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)