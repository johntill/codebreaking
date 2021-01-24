import random
import cipher_tools as tools

ngram_file = 'texts/Frequencies/english_quadgrams.txt'
score_text = tools.ngram_score_text

input_path = 'texts/plain_texts/'
output_path = 'texts/code_texts/'

input_files = ['subtest4.txt']

output_files_prefix = 'subtest'
output_files_start_at_number = 4

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def encrypt(text, key):
    key = ''.join(key)
    table = str.maketrans(alphabet, key)
    return text.translate(table)

for index, file in enumerate(input_files):
    input_file = input_path + file

    output_files_number = str(output_files_start_at_number + index)
    output_file_name = output_files_prefix + output_files_number + '.txt'
    output_file = output_path + output_file_name

    text = tools.import_cipher(input_file)
    text_len = len(text)

    attributes = tools.create_ngram_attributes(ngram_file, text_len)
    score = score_text(text, attributes)
    print(input_file, text_len, score, output_file)

    # key = [*alphabet]
    # random.shuffle(key)
    # print(key)
    # cipher = encrypt(text, key)
    #print(text)
    # print(cipher)
    # print()

    # Write text to output_file
    # with open(output_file, 'w') as f:
    #     f.write(text)

