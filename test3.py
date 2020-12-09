import timeit

code_to_test = """
import string
import re

cipher_file = 'texts/Plain_texts/plain5.txt'

with open(cipher_file) as f:
    text = f.read()
text = re.sub('[^A-Z]','', text.upper())

# letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
#        'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
#        'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

# arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
#        'P','Q','R','S','T','U','V','W','X','Y','Z')

arr = tuple(string.ascii_uppercase)
letters = {ch: index for index, ch in enumerate(arr)}

text = [letters[i] for i in text]

for _ in range(1):
    plain = [arr[ch] for ch in text]

plain = ''.join(plain)

#print(plain)

"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)