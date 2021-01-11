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

start = time.perf_counter()


for _ in range(1):
    cipher_bin = [letters[char] for char in text]
    char_positions = []
    for idx in range(key_len):
        char_positions.append([i for i, x in enumerate(cipher_bin) if x == idx])
    print(char_positions)
    key = [idx for idx in range(key_len)]
    print(key)
    plaintext = [key.index(idx) for idx in cipher_bin]
    print(plaintext)
    for idx1 in range(key_len - 1):
        for idx2 in range(idx1 + 1, key_len):
            ch1 = key[idx1]
            ch2 = key[idx2]
            for idx in char_positions[ch1]:
                plaintext[idx] = idx2
            for idx in char_positions[ch2]:
                plaintext[idx] = idx1
    print(plaintext)



#print(char_positions)
end = time.perf_counter()
print(f'{end-start}s')
