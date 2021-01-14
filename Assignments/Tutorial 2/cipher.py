def encrypt(text, shift):
    """ 
    Encrypts given text, shifted alphabetically by given shift amount;
    ignores non-alphabetic characters
     """
    encrypted_text = ""
    for letter in text:
        if letter.isalpha():
            shifted = ord(letter) + shift # first shift
            if letter.isupper():
                first_letter_ord = ord('A')
            else:
                first_letter_ord = ord('a')
            shifted -= first_letter_ord
            shifted %= 26 # then wrap around if necessary
            encrypted_text += chr(shifted + first_letter_ord) # then encode letter
        else:
            encrypted_text += letter # don't process non-alphabetic chars

    return encrypted_text

def decrypt(text, shift):
    """
    Decrypts given text. Ignores non-alphabetic characters.
    """
    decrypted_text = ""
    for letter in text:
        if letter.isalpha():
            shifted = ord(letter) - shift # first shift
            if letter.isupper():
                first_letter_ord = ord('A')
            else:
                first_letter_ord = ord('a')
            shifted -= first_letter_ord
            shifted %= 26 # then wrap around if necessary
            decrypted_text += chr(shifted + first_letter_ord) # then decode letter    
        else:
            decrypted_text += letter

    return decrypted_text

if __name__ == "__main__":
    assert decrypt(encrypt("apple", 1), 1) == "apple"
    assert decrypt(encrypt("zebra", 1), 1) == "zebra"
    assert decrypt(encrypt("This is some text", 10), 10) == "This is some text"
    with open("mobydick.txt", 'r') as f:
        text = f.read() # must store copy of text to avoid calling f.read() twice
        assert decrypt(encrypt(text, 13), 13) == text