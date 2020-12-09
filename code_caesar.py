class Caesar:

    def __init__(self, shift):
        self.shift = shift % 26
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encipher(self, text):
        shifted_alphabet = (self.alphabet[self.shift:]
                            + self.alphabet[:self.shift])
        table = str.maketrans(self.alphabet, shifted_alphabet)
        return text.translate(table)

    def decipher(self, text):
        shifted_alphabet = (self.alphabet[self.shift:]
                            + self.alphabet[:self.shift])
        table = str.maketrans(shifted_alphabet, self.alphabet)
        return text.translate(table)
