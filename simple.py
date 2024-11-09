# examples/intro/secure.py

from simplefhe import (
    encrypt, decrypt,
    generate_keypair,
    set_public_key, set_private_key, set_relin_keys,
    display_config,
    load_encrypted_str,
)

# In a real application, the keypair would be generated once,
# and only the public key would be provided to the server.
# A more realistic example is given later.
display_config()
public_key, private_key, relin_keys = generate_keypair()
set_public_key(public_key)
set_relin_keys(relin_keys)
display_config()

set_private_key(private_key)

display_config()

soma = 0
# The server
def process(x):
    global soma
    soma += x
    print(len(x.value))
    return x**3 - 3*x + 1


# The client
sensitive_data = [-30, -5, 17, 28]
for entry in sensitive_data:
    encrypted = encrypt(entry) # Encrypt the data...
    result = process(encrypted) # Process the encrypted data on the server...
    print(entry, decrypt(result)) # Decrypt the result on the client.
print(decrypt(soma)) # Decrypt the sum on the client.
print(sum(sensitive_data))

lol = [encrypt(ord(x)).value for x in 'encripta ai meu pai']
# lol = [decrypt(load_encrypted_str(x)) for x in lol]
# lol = [chr(x) for x in lol]

xau = [encrypt(ord(x)).value for x in ' pega na minha fubanga']
# xau = [decrypt(load_encrypted_str(x)) for x in xau]
# xau = [chr(x) for x in xau]

res = lol+xau
# print(res)
print([len(x) for x in res])
res = [decrypt(load_encrypted_str(x)) for x in res]
print(res)
res = [chr(x) for x in res]

print(''.join(res))

print(encrypt(25)+encrypt(30))
# print((encrypt(25)+encrypt(30)).value)
print(decrypt(encrypt(25)+encrypt(30)))

def encrypt_str(string: str) -> list[str]:
    return [encrypt(ord(x)).value for x in string]
voto = encrypt_str("Robson PMDB")
robson = encrypt_str("PMDB Robson")
# char -(ord)-> int -(encrypt)-> EncryptedInt -(operations: + - * / % //)-> EncryptedInt -(decrypt)-> int -(chr)-> char
def mix(elements: str) -> int:
    return sum(elements*(i+1) if i % 2 == 0 else -elements*(i+1) for i, elements in enumerate(elements))

voto = mix(load_encrypted_str(x) for x in voto)
robson = mix(load_encrypted_str(x) for x in robson)

print(decrypt(voto))
print(decrypt(robson))
print(decrypt(voto) == decrypt(robson))

# print([decrypt(load_encrypted_str(x)) for x in encrypt_str("Robson PMDB")] == [decrypt(load_encrypted_str(x)) for x in voto])
# print([decrypt(load_encrypted_str(x)) for x in encrypt_str("Robson PMDB")])
# print([decrypt(load_encrypted_str(x)) for x in voto])