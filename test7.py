import time

def segment_slide(fixed_key):
    for l in range(1, key_len):
        for p in range(key_len - l):
            for s in range(1, key_len - l - p + 1):
                key = fixed_key[0:p] + fixed_key[p+l:]
                key = key[0:p+s] + fixed_key[p:p+l] + key[p+s:]
                yield key

def segment_slide2(fixed_key):
    for l in range(1, key_len):
        for p in range(key_len - l):
            key = fixed_key[0:p] + fixed_key[p+l:]
            segment = fixed_key[p:p+l]
            for s in range(1, key_len - l - p + 1):
                yield key[0:p+s] + segment + key[p+s:]

def bi_score(key):
    print(f'Using Bigrams: {key}')

def tri_score(key):
    print(f'Using Trigrams: {key}')
    
    

key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#key = 'ABCD'
key_len = len(key)

start = time.perf_counter()
#print(key)

for _ in range(1):
    count = 0
    for new_key in segment_slide2(key):
        #print(new_key)
        count += 1

#score_using = 'bigrams'
score_using = 'trigrams'

ev_file = 'texts/Frequencies/english_' + score_using + '.txt'
scoring_function = bi_score if score_using == 'bigrams' else tri_score
scoring_function(key)
print(ev_file)

print(count)

end = time.perf_counter()
print(f'{end-start}s')
