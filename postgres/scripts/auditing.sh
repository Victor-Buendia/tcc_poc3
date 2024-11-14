#! /bin/bash

echo """
shared_preload_libraries = 'pgaudit'
log_statement = 'all'
log_line_prefix = '%m [%p] %q%u@%d '
""" >> postgres/postgres_data/postgresql.conf