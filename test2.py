import timeit

code_to_test = """
import re

filename = 'texts/plain_texts/warandpeace.txt'

with open(filename, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()

text = re.sub('[^A-Z]','', text.upper())

def frequency_analysis(text, alphabet=None):
    if not alphabet: alphabet = set(text)
    return {char : text.count(char) for char in alphabet}

def frequency_analysis2(text, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    return {char : text.count(char) for char in alphabet}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

#print(alphabet)

for i in range(100):
    freq = frequency_analysis(text, alphabet)

#print(freq)
"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)



    
        