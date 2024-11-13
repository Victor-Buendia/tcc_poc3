#! /bin/bash

### Client Certificate ###
# Generate private key for the client
openssl genpkey -algorithm RSA -out consumer.key

# Secure the private key
chmod 600 consumer.key

# Generate a certificate signing request (CSR) for the client
openssl req -new -key consumer.key -out consumer.csr -subj "/CN=consumer"

# Sign the client certificate with the CA certificate and key
openssl x509 -req -in consumer.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out consumer.crt -days 365