import time
import cipher_tools as tools

cipher_file = 'texts/Code_texts/subtest2.txt'

#text = tools.import_cipher(cipher_file)
text = 'HELLOWORLD'
text_len = len(text)

alphabet = tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
key_len = len(alphabet)
#print(key_len)
letters = {ch: index for index, ch in enumerate(alphabet)}

iterator = (letters[char] for char in text)

start = time.perf_counter()
for _ in range(1):
    quadgram_val = iterator.__next__()
    print(quadgram_val)
    quadgram_val = (quadgram_val << 5) + iterator.__next__()
    print(quadgram_val)
    quadgram_val = (quadgram_val << 5) + iterator.__next__()
    print(quadgram_val)
    quadgrams = [0 for cntr in range(32 * 32 * 32 * 32)]
    print(quadgrams)


#print(a)
#print(b)
#print(c)
#print(d)
end = time.perf_counter()
print(f'{end-start}s')