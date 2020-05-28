from math import log10

class NgramScore(object):
    def __init__(self, ngram_file, sep=' '):
        self.ngrams = {}
        with open(ngram_file, 'r', encoding='utf8', errors='ignore') as f:
            for line in f:
                ngram, _, count = line.partition(sep)
                self.ngrams[ngram] = float(count)
        self.count_total = sum(self.ngrams.values())
        self.floor = log10(0.01 / self.count_total)
        self.ngram_len = len(ngram)
        for ngram in self.ngrams.keys():
            self.ngrams[ngram] = log10(self.ngrams[ngram] / self.count_total)

    def score(self, text):
        score = 0
        for i in range(len(text) - self.ngram_len + 1):
            try:
                score += self.ngrams[text[i:i+self.ngram_len]]
            except:
                score += self.floor
        return score
