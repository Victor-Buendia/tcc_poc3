#! /bin/bash

echo """
ssl = on
ssl_cert_file = '/etc/postgresql/certs/server.crt'
ssl_key_file = '/etc/postgresql/certs/server.key'
""" >> postgres/postgres_data/postgresql.conf

sed -i -e '/^host all/ s/^.*//' postgres/postgres_data/pg_hba.conf 
echo """
# TYPE  DATABASE        USER            ADDRESS                 METHOD
hostssl all             all             0.0.0.0/0               md5
hostnossl all           all             0.0.0.0/0               reject
""" >> postgres/postgres_data/pg_hba.conf