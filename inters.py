# examples/intro/secure.py

from universidade.libs.simplefhe import (
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
    print(x.value)
    return x**3 - 3*x + 1

import sys
sys.set_int_max_str_digits(1_000_000_000)  # Set to a higher limit, adjust if necessary
a = 0
# The client
sensitive_data = [-30, -5, 17, 28]
for entry in sensitive_data:
    encrypted = encrypt(entry)
    a += encrypted

print(decrypt(a))
with open('soma.txt', 'w') as f:
    f.write(str((a.value)))