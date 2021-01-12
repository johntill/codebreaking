import time
import random
import cipher_tools as tools

cipher_file = 'texts/Code_texts/subtest3.txt'
ngram_file = 'texts/Frequencies/english_quadgrams.txt'


text = tools.import_cipher(cipher_file)
#text = 'ROCKETWEAPONSARENOTNEWINWARMARETHECHINESEUSEDROCKETPROPELLEDARROWSOVERATHOUSANDBEARSAGO'
text_len = len(text)

attributes = tools.create_ngram_attributes(ngram_file, text_len)
score_text = tools.ngram_score_text

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decrypt(cipher_text, key, alphabet):
    key = ''.join(key)
    table = str.maketrans(key, alphabet)
    return cipher_text.translate(table)

key = 'HRFSALDGJUMNBPQTIVWXYZKEOC'
#key = 'HOFSALDGJUMNBPQTIVWXYZKERC'
#key = 'HOFSABDGJUMNLPQTIVWXYZKERC'

start = time.perf_counter()

plain_text = decrypt(text, key, alphabet)
print(plain_text)
score = score_text(plain_text, attributes)
print(score)


end = time.perf_counter()
print(f'{end-start}s')
