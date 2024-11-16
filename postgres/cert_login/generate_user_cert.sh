#! /bin/bash

### Client Certificate ###
# Generate private key for the client
openssl genpkey -algorithm RSA -out consumer.key
openssl genpkey -algorithm RSA -out professor.key

# Secure the private key
chmod 600 consumer.key
chmod 600 professor.key

# Generate a certificate signing request (CSR) for the client
openssl req -new -key consumer.key -out consumer.csr -subj "/CN=consumer"
openssl req -new -key professor.key -out professor.csr -subj "/CN=professor"

# Sign the client certificate with the CA certificate and key
openssl x509 -req -in consumer.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out consumer.crt -days 365
openssl x509 -req -in professor.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out professor.crt -days 365