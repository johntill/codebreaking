import timeit

code_to_test = """
import re

filename = 'texts/plain_texts/plainshort2.txt'

with open(filename, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

text = re.sub('[^A-Z]','', text.upper())

def frequency_analysis(text, alphabet=None):
    if not alphabet: alphabet = set(text)
    return {char : text.count(char) for char in alphabet}

def frequency_analysis2(text, alphabet=set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')):
    return {char : text.count(char) for char in alphabet}

def frequency_analysis3(text):
    return {char : text.count(char) for char in set(text)}

def frequency_analysis4(text):
    return {char : text.count(char) for char in alphabet}

def frequency_analysis5(text, alphabet):
    text_count = text.count
    return {char : text_count(char) for char in alphabet}

#alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

#print(alphabet)

for i in range(300_000):
    freq = frequency_analysis5(text, alphabet)
    #freq = frequency_analysis2(text)

#print(freq)
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)



    
        