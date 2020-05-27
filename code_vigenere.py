import string

class Vigenere:

    def __init__(self, key):
        self.key = ''.join(key)
        self.key = self.key.upper()
        self.key_len = len(self.key)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letters = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
           'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,
           'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,'Y':24,'Z':25}

    def encipher(self, text):
        trans_text = [None] * len(text)
        for i, c in enumerate(self.key):
            section = text[i::self.key_len]
            shifted_alphabet = (self.alphabet[self.letters[c]:]
                                + self.alphabet[:self.letters[c]])
            table = str.maketrans(self.alphabet, shifted_alphabet)
            trans_text[i::self.key_len] = section.translate(table)
        return ''.join(trans_text)

    def decipher(self, text):
        trans_text = [None] * len(text)
        for i, c in enumerate(self.key):
            section = text[i::self.key_len]
            shifted_alphabet = (self.alphabet[self.letters[c]:]
                                + self.alphabet[:self.letters[c]])
            table = str.maketrans(shifted_alphabet, self.alphabet)
            trans_text[i::self.key_len] = section.translate(table)
        return ''.join(trans_text)
