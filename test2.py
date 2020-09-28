import timeit

code_to_test = """
import re
from collections import Counter

filename = 'texts/plain_texts/plainshort2.txt'

with open(filename, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

text = re.sub('[^A-Z]','', text.upper())

def frequency_analysis(text, alphabet=None):
    if not alphabet: alphabet = set(text)
    text_count = text.count
    return {char : text_count(char) for char in alphabet}

def frequency_analysis2(text, alphabet=set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')):
    text_count = text.count
    return {char : text_count(char) for char in alphabet}

def frequency_analysis3(text):
    return {char : text.count(char) for char in set(text)}

def frequency_analysis4(text):
    return {char : text.count(char) for char in alphabet}

def frequency_analysis5(text, alphabet):
    text_count = text.count
    return {char : text_count(char) for char in alphabet}

def frequency_analysis6(text, alphabet):
    return {char : text.count(char) for char in alphabet}

#alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

#print(alphabet)

for i in range(200_000):
    #freq = frequency_analysis2(text, alphabet)
    #freq = frequency_analysis(text)
    freq = Counter(text)

#print(freq)
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)



    
        