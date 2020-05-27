import re

class PolybiusSquare:

    def __init__(self, key='ABCDEFGHIKLMNOPQRSTUVWXYZ', chars='ADFGX'):
        assert len(key) == len(chars) ** 2
        self.key = list(key)
        self.pairs = [char+char2 for char in chars for char2 in chars]

    def encipher(self, text):
        if 'J' not in self.key:
            text = re.sub(r'[J]', 'I', text)
        vocab = dict(zip(self.key, self.pairs))
        return ''.join([vocab[letter] for letter in text])

    def decipher(self, text):
        text_len = len(text)
        assert text_len % 2 == 0
        vocab = dict(zip(self.pairs, self.key))
        return ''.join([vocab[text[c:c+2]] for c in range(0, text_len, 2)])
