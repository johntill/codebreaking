from time import perf_counter
import cipher_tools as ct

start = perf_counter()

ngram_file = 'texts/Frequencies/english_quadgrams.txt'
filename = 'texts/Code_texts/enigma_medium2.txt'

text = ct.import_cipher(filename)
text_len = len(text)
#text = list(text)

letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,
           'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17,
           'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

arr = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
       'Q','R','S','T','U','V','W','X','Y','Z')

#text = [letters[i] for i in text]

#import ngram_score as ns
#fitness = ns.NgramScore(ngram_file)
#fitness_score = fitness.score

ngram_create_scoring_attributes = ct.ngram_create_scoring_attributes
ngram_score_text = ct.ngram_score_text

ngram_attributes = ngram_create_scoring_attributes(ngram_file, text_len)

for _ in range(20000):
    scores = ngram_score_text(text, ngram_attributes)
    #plain = ''.join([arr[ch] for ch in text])
    #scores = ngram_score_text(plain, ngram_attributes)
    #scores = fitness.score(plain)
    #scores = fitness_score(text)

#print(scores)

end = perf_counter()
time_taken = end - start
print(f'Time taken - {time_taken:.2f}s')