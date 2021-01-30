import re
from collections import Counter

# Name of file containing cipher.
cipher_file = 'texts/Code_texts/enigma_FHPQX.txt'

with open(cipher_file) as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())
text_len = len(text)

settings = ('M', 'D', 'V')
#settings = ('S', 'D', 'V')
rotors = (4, 2, 3)
reflector = 'B'
ringstellung = ('A', 'T', 'O')
#ringstellung = ('A', 'A', 'A')
#steckers = ([(4,25),(17,22),(12,21),(8,20),(1,11),(15,23),(9,14)])
#steckers = [(0,3),(4,7),(6,24),(8,12),(10,13),(11,17),(14,25),(16,21),(19,23),(20,22)] # FHPQX
steckers = []

letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
       'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
       'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
       'P','Q','R','S','T','U','V','W','X','Y','Z')

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
reflectorkey = ["EJMZALYXVBWFCRQUONTSPIKHGD",
                "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                "FVPJIAOYEDRZXWGCTKUQSBNMHL"]

rotorkey = [[letters[i] for i in rotor] for rotor in rotorkey]
invrotor = [[letters[i] for i in rotor] for rotor in invrotor]

notch = ((16,),(4,),(21,),(9,),(25,),(25,12),(25,12),(25,12))

settings = [letters[i] for i in settings]
print(settings)
rotors = [i-1 for i in rotors]
reflector = tuple([letters[i] for i in reflectorkey[letters[reflector]]])
ringstellung = [letters[i] for i in ringstellung]

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
    #print(ch, settings)
    return (key[ch] - offset) % 26

def encipher_char(ch):
    #print(ch, settings)
    #print()
    advance_rotor()
    if steckers:
        ch = apply_steckers(ch)
    for i in (2, 1, 0):
        #print("-"*10)
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, rotorkey[rotors[i]], offset)
        #print(ch, settings)
    #print()
    ch = reflector[ch]
    #print(ch, settings)
    #print()
    for i in (0, 1, 2):
        #print("-"*10)
        offset = settings[i] - ringstellung[i]
        ch = apply_rotor(ch, invrotor[rotors[i]], offset)
        #print(ch, settings)
    if steckers:
        ch = apply_steckers(ch)
    #print()
    return ch

def calculate_IC(frequencies, N):
    frequency_values = frequencies.values()
    f = sum(
        [v * (v - 1) for v in frequency_values]
    )
    return f / N

#text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#text = "AAAAA"
#text = "MDYLSD"
#text = 'ABCDEF'

text = [letters[i] for i in text]

N = text_len * (text_len - 1)

for n in range(1000):
    plain = [encipher_char(ch) for ch in text]


plain = [arr[ch] for ch in plain]
plain = ''.join(plain)
frequencies = Counter(plain)
IC = calculate_IC(frequencies, N)
print(IC)
print(plain)

# with open('enigmacipher2.txt', 'w') as f:
#     f.write(plain)

