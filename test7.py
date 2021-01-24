import time

scoring_functions = {
    'bigrams': (score_bigrams, 'texts/Frequencies/english_bigrams.txt'),
    'trigrams': (score_trigrams, 'texts/Frequencies/english_trigrams.txt')
}

def set_scoring_method(score_using):
    ev_file = 'texts/Frequencies/english_' + score_using + '.txt'
    scoring_function = score_bigrams if score_using == 'bigrams' else score_trigrams
    return scoring_function, ev_file

def set_scoring_method2(score_using):
    scoring_function, ev_file = scoring_functions[score_using]
    return scoring_function, ev_file

def score_bigrams(ev_file):
    print(f'Using Bigrams - {ev_file}')

def score_trigrams(ev_file):
    print(f'Using Trigrams - {ev_file}')
    

#score_using = 'bigrams'
score_using = 'trigrams'

start = time.perf_counter()
for _ in range(5_000_000):
    scoring_function, ev_file = set_scoring_method2(score_using)
    
#scoring_function(ev_file)

end = time.perf_counter()
print(f'{end-start}s')
