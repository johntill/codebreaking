import cipher_tools as ct
import code_caesar as caesar

cipher_file = 'texts/Code_texts/Caesartest1.txt'
ev_file = 'texts/Frequencies/english_monograms.txt'

# Function that tries all 26 different possibilities of the Caesar
# cipher then uses the Chi squared score of each to display the correct
# translation.
def score_caesar(text, ngrams_ev, shift):
    plaintext = caesar.Caesar(shift).decipher(text)
    freq = ct.frequency_analysis(plaintext)
    chi_two = ct.chi_squared(freq, ngrams_ev)    
    print(f'{shift:02} : {plaintext[:15]} : {chi_two:.4f}')
    return chi_two, shift

def main():
    text = ct.import_cipher(cipher_file)
    text_len = len(text)

    ngrams_ev = ct.expected_values(ev_file, text_len)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    scores = [score_caesar(text, ngrams_ev, shift) for shift in range(26)]
    best_shift = sorted(scores)[0][1]
    plain_text = caesar.Caesar(best_shift).decipher(text)
    print(f"\nOriginal shift = {alphabet[best_shift]} ({best_shift})\n")
    print(plain_text.lower())

if __name__ == "__main__":
    main()