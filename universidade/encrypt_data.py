import os
import psycopg2
from logger.log import get_logger

log = get_logger('encrypt_data')

# Get the encryption key from an environment variable
encryption_key = os.environ.get('AES_KEY_B64')

# Your database connection
conn = psycopg2.connect("dbname={PGDATABASE} user={PGUSER} password={PGPASSWORD} host={PGHOST}".format(
    PGDATABASE=os.environ.get('PGDATABASE'),
    PGUSER=os.environ.get('PGUSER'),
    PGPASSWORD=os.environ.get('PGPASSWORD'),
    PGHOST=os.environ.get('PGHOST')
))
cur = conn.cursor()

# Encrypting data
query = f"""
CREATE TABLE pii.discentes AS (
    SELECT
        id_discente,
        data_nascimento,
        pgp_sym_encrypt(cpf, '{encryption_key}') AS cpf,
        nome,
        pgp_sym_encrypt(email, '{encryption_key}') AS email,
        pgp_sym_encrypt(telefone, '{encryption_key}') AS telefone,
        cartao,
        token_cartao,
        senha
    FROM public.discentes
);
"""
# SELECT pgp_sym_decrypt(cpf::BYTEA, 'key') FROM discentes;

cur.execute(query)
conn.commit()
cur.close()
conn.close()
log.info("Data encrypted successfully")
