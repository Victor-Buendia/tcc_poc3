import os
from ff3 import FF3Cipher

def generate_random_token(length: int) -> str:
    return os.urandom(length).hex()

def generate_pseudorandom_tokens(key, tweak, data) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    cipher = FF3Cipher.withCustomAlphabet(key, tweak, alphabet)
    words = data.split()
    encrypted_words = [cipher.encrypt(w.ljust(4, '_')) for w in words]
    return " ".join(encrypted_words)

def decrypt_pseudorandom_tokens(key, tweak, data) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
    cipher = FF3Cipher.withCustomAlphabet(key, tweak, alphabet)
    words = data.split()

    decrypted_words = [cipher.decrypt(w).rstrip('_') for w in words]
    return " ".join(decrypted_words)

if __name__ == '__main__':
    key = os.environ.get('TOKENIZATION_KEY')
    tweak = os.environ.get('TOKENIZATION_TWEAK')

    print(f"Key: {key}, Tweak: {tweak}")

    data = "This is a test with repeated test words test test test"
    print(generate_pseudorandom_tokens(key, tweak, data))
    print(decrypt_pseudorandom_tokens(key, tweak, generate_pseudorandom_tokens(key, tweak, data)))
