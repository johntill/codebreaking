import timeit

code_to_test = """
from collections import Counter

cipher_file = 'texts/Code_texts/enigma_medium2.txt'


# Loads cipher text, removes any punctuation and converts to uppercase
with open(cipher_file) as f:
    text = f.read()

#print(text)

text_len = len(text)
N = text_len * (text_len - 1)
#print(text_len)

letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
   'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
   'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
       'P','Q','R','S','T','U','V','W','X','Y','Z')

numbers = [letters[i] for i in text]

#print(text)

import array

arr1 = array.array('I', numbers)

alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
nums = set(range(26))

def frequency_analysis(arr1):
    return {char: arr1.count(char) for char in nums}

def frequency_analysis2(numbers):
    return {char : numbers.count(char) for char in nums}

def frequency_analysis3(text):
    return {char : text.count(char) for char in alphabet}

def frequency_analysis4(numbers):
    freq = Counter()
    for num in numbers:
        freq[num] += 1
    return freq

def frequency_analysis5(plain):
    plain = [arr[ch] for ch in plain]
    plain = ''.join(plain)
    return {char : plain.count(char) for char in alphabet}

def calculate_IC(frequencies, N):
    f = 0
    for v in frequencies.values():
        f += v * (v - 1)
    return f / N

for _ in range(1):
    #freq = frequency_analysis(arr1)
    #freq = frequency_analysis2(numbers)
    #freq = frequency_analysis3(text)
    #freq = frequency_analysis4(numbers)
    #freq = frequency_analysis5(numbers)
    freq = Counter(numbers)
    IC = calculate_IC(freq, N)

print(IC)
print(freq)
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)