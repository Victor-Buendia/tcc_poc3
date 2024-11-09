import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


def generate_key_b64():
    key = os.urandom(32)
    return base64.b64encode(key).decode("utf-8")


def generate_iv_b64():
    iv = os.urandom(16)
    return base64.b64encode(iv).decode("utf-8")


def encrypt_data_b64(key, iv_b64, data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    elif isinstance(data, dict):
        data = str(data).encode("utf-8")
    elif isinstance(data, int):
        data = str(data).encode("utf-8")

    key = base64.b64decode(key)

    iv = base64.b64decode(iv_b64.encode("utf-8"))
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_b64 = base64.b64encode(encrypted_data).decode("utf-8")

    return encrypted_b64


def decrypt_data(key, iv_b64, encrypted_b64):
    key = base64.b64decode(key)
    iv = base64.b64decode(iv_b64)
    encrypted_data = base64.b64decode(encrypted_b64)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode("utf-8")


if __name__ == '__main__':
    # key = generate_key()
    # iv_b64 = generate_iv()
    key = "sV7Ln1GfX0zsAcMw2+OWAkHZevVyodHPE3eTP7BnTLs="
    iv_b64 = "XZV9yKNz2RrPz2m7OJ/SCw=="
    encrypted_b64 = encrypt_data_b64(key, iv_b64, "Hello, this is secret!")
    decrypted = decrypt_data(key, iv_b64, encrypted_b64)

    print("Key:", key)
    print("IV:", iv_b64)
    print("Original Message:", "Hello, this is secret!")
    print("Encrypted Message:", encrypted_b64)
    print("Decrypted Message:", decrypted)
