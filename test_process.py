from math import log10
from time import perf_counter

start = perf_counter()

ngram_file = 'texts/Frequencies/english_quintgrams.txt'

ngrams = {}
with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
        for line in f:
            ngram, _, count = line.partition(' ')
            ngrams[ngram] = float(count)
count_total = sum(ngrams.values())
floor = log10(0.01 / count_total)
ngram_len = len(ngram)
for ngram, count in ngrams.items():
    ngrams[ngram] = log10(count / count_total)

#print(ngrams)

end = perf_counter()
time_taken = end - start
print(f'Time taken - {time_taken:.2f}s')