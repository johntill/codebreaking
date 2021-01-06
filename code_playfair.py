import re

class Playfair:

    def __init__(self, key='ABCDEFGHIKLMNOPQRSTUVWXYZ'):
        self.key = ''.join(key)
        self.key = self.key.upper()

    def encipher_pair(self, a, b):
        if a == b:
            b = 'X'
        arow, acol = divmod(self.key.index(a), 5)
        brow, bcol = int(self.key.index(b) / 5), self.key.index(b) % 5
        if arow == brow:
            return (self.key[arow*5 + (acol+1) % 5]
                  + self.key[brow*5 + (bcol+1) % 5])
        elif acol == bcol:
            return (self.key[((arow+1) % 5)*5 + acol]
                  + self.key[((brow+1) % 5)*5 + bcol])
        else:
            return self.key[arow*5 + bcol] + self.key[brow*5 + acol]

    def decipher_pair(self, a, b):
        arow, acol = divmod(self.key.index(a), 5)
        brow, bcol = int(self.key.index(b) / 5), self.key.index(b) % 5
        if arow == brow:
            return (self.key[arow*5 + (acol-1) % 5]
                  + self.key[brow*5 + (bcol-1) % 5])
        elif acol == bcol:
            return (self.key[((arow-1) % 5)*5 + acol]
                  + self.key[((brow-1) % 5)*5 + bcol])
        else:
            return self.key[arow*5 + bcol] + self.key[brow*5 + acol]

    def encipher(self, text):
        text = re.sub(r'[J]', 'I', text)
        text_len = len(text)
        if text_len % 2:
            text += 'X'
        return ''.join([self.encipher_pair(text[c], text[c+1])
                for c in range(0, text_len, 2)])

    def decipher(self, text):
        return ''.join([self.decipher_pair(text[c], text[c+1])
                for c in range(0, len(text), 2)])
