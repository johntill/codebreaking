import time
import cipher_tools as tools
import ngram_score as ns

cipher_file = 'texts/Plain_texts/dracula.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'

text = tools.import_cipher(cipher_file)
text_len = len(text)

attributes = tools.create_ngram_attributes(ngram_file, text_len)
score_text = tools.ngram_score_text

#fitness = ns.NgramScore(ngram_file)

start = time.perf_counter()
for _ in range(5):
    score = score_text(text, attributes)
    #score = fitness.score(text)

# print(score)


end = time.perf_counter()
print(f'{end-start}s')