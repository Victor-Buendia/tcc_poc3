#! /bin/bash

### Certificate Authority (Self-Signed) ### 
# Generate private key for the Certificate Authority (CA)
openssl genpkey -algorithm RSA -out ca.key -pkeyopt rsa_keygen_bits:2048

# Secure the private key
chmod 600 ca.key

# Generate the CA certificate with a unique CN
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj "/C=BR/ST=DF/L=UNB/O=FCTE/CN=TCC2"
# https://stackoverflow.com/questions/53104296/unknown-ca-with-self-generated-ca-certificates-and-client-server


### Server Certificate ###
# Generate private key for the server
openssl genpkey -algorithm RSA -out server.key -pkeyopt rsa_keygen_bits:2048

# Secure the private key
chmod 600 server.key

# Generate a certificate signing request (CSR) for the server
openssl req -new -key server.key -out server.csr -subj "/CN=localhost"

# Sign the server certificate with the CA certificate and key
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
