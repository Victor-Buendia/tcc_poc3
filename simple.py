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
