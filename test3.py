import string
import re
from time import perf_counter

#filename = 'texts/Plain_texts/warandpeace.txt'
filename = 'texts/Plain_texts/plain5.txt'


with open(filename, 'r', encoding='utf8', errors='ignore') as f:
    text = f.read()
# Removes punctuation & whitespace, converts to all UPPERCASE
text = re.sub('[^A-Z]','', text.upper())



# letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
#        'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
#        'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

# arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
#        'P','Q','R','S','T','U','V','W','X','Y','Z')

#arr = tuple(string.ascii_uppercase)
arr = string.ascii_uppercase

letters = {ch: index for index, ch in enumerate(arr)}

new_text = [letters[i] for i in text]

start = perf_counter()
for _ in range(1):
    plain = [arr[ch] for ch in new_text]





end = perf_counter()
#plain = ''.join(plain)

#print(plain)


time_taken = end - start
print(f'Time taken - {time_taken}s')