#! /bin/bash

# Generate private key
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:2048

# Secure the private key
chmod 600 server.key

# Generate a certificate signing request (CSR)
openssl req -new -key server.key -out server.csr

# Generate the self-signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt