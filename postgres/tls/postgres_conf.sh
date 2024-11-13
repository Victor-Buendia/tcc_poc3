#! /bin/bash

echo """
ssl = on
ssl_ca_file = '/etc/postgresql/certs/ca.crt'
ssl_cert_file = '/etc/postgresql/certs/server.crt'
ssl_key_file = '/etc/postgresql/certs/server.key'
""" >> postgres/postgres_data/postgresql.conf

sed -i -e '/^host all/ s/^.*//' postgres/postgres_data/pg_hba.conf 
echo """
# TYPE      DATABASE        USER            ADDRESS                 METHOD
hostssl     all             postgres        0.0.0.0/0               md5
hostnossl   all             all             0.0.0.0/0               reject
hostssl     all             consumer        0.0.0.0/0               cert
""" >> postgres/postgres_data/pg_hba.conf