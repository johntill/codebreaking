class ColumnarTransposition:

    def __init__(self, key):
        self.key = key
        self.key_len = len(self.key)
        self.ord_key = sorted(self.key)

    def encipherICT(self, text):
        return ''.join([text[self.key.index(char)::self.key_len]
                for char in self.ord_key])

    def encipherCCT(self, text):
        text_len = len(text)
        remainder = text_len % self.key_len
        if remainder != 0:
            text += 'X' * (self.key_len - remainder)
        return ''.join([text[self.key.index(char)::self.key_len]
                for char in self.ord_key])

    def decipher(self, text):
        text_len = len(text)
        column_len = text_len // self.key_len
        remainder = text_len % self.key_len
        plain = [None] * text_len
        position = 0
        for char in self.ord_key:
            i = self.key.index(char)
            if i < remainder:
                new_column = column_len + 1
            else:
                new_column = column_len
            plain[i::self.key_len] = text[position:position + new_column]
            position += new_column
        return ''.join(plain)
