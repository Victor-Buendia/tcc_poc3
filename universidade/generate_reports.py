import duckdb
import pandas as pd
import math

from libs import *
from logger.log import get_logger

log = get_logger('ingest_data')

load_public_key('keys/public.key')
load_private_key('keys/private.key')
load_relin_keys('keys/relin.key')
display_config()

tokenization_key = os.environ.get('TOKENIZATION_KEY')
tokenization_tweak = os.environ.get('TOKENIZATION_TWEAK')

tokenize = lambda data: generate_pseudorandom_tokens(tokenization_key, tokenization_tweak, data)
decrypt_fhe = lambda data: decrypt(load_encrypted_str(data))

conn = duckdb.connect(database=os.environ.get('DUCKDB_PATH'), read_only=False)
conn.execute("""
    INSTALL postgres;
    LOAD postgres;
    ATTACH '' AS psql (TYPE POSTGRES);
""")


### MÉDIA SALARIAL DE PROFESSORES POR CURSO ###
docentes = conn.execute("SELECT * FROM psql.public.docentes").fetch_df()
docentes['salario'] = docentes['salario'].apply(load_encrypted_str)

# Step 1: Compute sum of 'salario' for each 'curso' and decrypt aggregated value
media_salarial = docentes.groupby('curso')['salario'].apply(lambda x: sum(x)).apply(decrypt)

# Step 2: Convert Pandas Series to DataFrame to allow adding new columns
media_salarial = media_salarial.reset_index()
media_salarial.columns = ['curso', 'salario']  # Rename columns for clarity

# Step 3: Calculate the number of professors per course
media_salarial['qtd_professores'] = docentes.groupby('curso').size().values

# Step 4: Compute average salary
media_salarial['media_salarial'] = round(media_salarial['salario'] / media_salarial['qtd_professores'])

# Step 5: Drop unnecessary columns
media_salarial_df = media_salarial.drop(columns=['qtd_professores', 'salario'])

# Write the DataFrame to DuckDB
print(media_salarial)
conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.media_salarial_docentes AS (
        SELECT * FROM media_salarial_df ORDER BY media_salarial DESC
    );
""")

### MÉDIA DE NOTA DE ALUNOS POR CURSO ###
disciplinas = conn.execute("SELECT * FROM psql.public.matriculadisciplinas").fetch_df()

# Step 1: Filter out rows with missing 'nota' values and load encrypted values
media_notas = disciplinas[disciplinas['nota'].notnull()]
media_notas['nota'] = media_notas['nota'].apply(load_encrypted_str)

# Step 2: Decrypt 'nota' values
media_notas = media_notas.groupby('semestre')['nota'].apply(sum).apply(decrypt).reset_index()
media_notas.columns = ['semestre', 'nota']

# Step 3: Calculate the number of students per semester and compute average of 'nota'
media_notas['qtd_alunos'] = disciplinas.groupby('semestre').size().values
media_notas['media_notas'] = round(media_notas['nota'] / media_notas['qtd_alunos'], 2)

# Step 4: Drop unnecessary columns
media_notas_df = media_notas.drop(columns=['qtd_alunos', 'nota'])

# Step 5: Print the DataFrame and write it to DuckDB
print(media_notas)
conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.media_notas_alunos AS (
        SELECT * FROM media_notas_df ORDER BY semestre ASC
    );
""")


### PUBLICAÇÃO DE SALÁRIOS ###
professores = conn.execute("SELECT D.*, P.data_nascimento FROM psql.public.docentes D JOIN psql.pii.docentes P ON D.matricula = P.matricula").fetch_df()

professores['salario'] = professores['salario'].apply(load_encrypted_str).apply(decrypt)

professores['idade'] = professores['data_nascimento'].apply(lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days // 365)
professores = professores.drop(columns=['senha', 'data_nascimento'])


conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.professores AS (
        SELECT * FROM professores ORDER BY matricula
    );
""")

new_professores = conn.execute("SELECT D.*, P.data_nascimento FROM psql.public.docentes D JOIN psql.pii.docentes P ON D.matricula = P.matricula").fetch_df()

new_professores['matricula'] = new_professores['matricula'].apply(lambda x: generate_random_token(15))
new_professores['idade'] = new_professores['data_nascimento'].apply(lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days // 365)
new_professores['idade'] = new_professores['idade'].apply(lambda x: '> 40' if x > 40 else '<= 40')

new_professores['salario'] = new_professores['salario'].apply(load_encrypted_str).apply(decrypt)
new_professores['salario'] = new_professores['salario'].apply(lambda x: round(round(x/1000)/10)*10*1000)

new_professores = new_professores.drop(columns=['nacionalidade', 'especializacao', 'data_nascimento', 'senha', 'curso'])

# conn.execute("""
#     CREATE OR REPLACE TABLE psql.relatorios.new_professores AS (
#         SELECT * FROM new_professores WHERE genero != 'Outro' ORDER BY genero, idade, salario
#     );
# """)


# Calculate L-diversity for sensitive attribute 'salario'
L = 1  # Define the L threshold

# Step 1: Group by quasi-identifiers (genero, idade)
grouped = new_professores.groupby(['genero', 'idade'])

# Step 2: Calculate diversity of 'salario' in each group
diversity = grouped['salario'].nunique()

# Step 3: Identify groups that conform to L-diversity
l_diverse = diversity >= L

# Step 4: Filter rows that belong to L-diverse groups
# Get the groups that meet L-diversity
conforming_groups = diversity[l_diverse].index

# Filter the DataFrame for conforming groups
new_professores_l_diverse = new_professores[
    new_professores.set_index(['genero', 'idade']).index.isin(conforming_groups)
]

non_conforming_groups = diversity[~l_diverse]
print("Non-conforming groups:\n", non_conforming_groups)

# Optional: Save the L-diverse DataFrame back to your database
conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.new_professores_l_diverse AS (
        SELECT * FROM new_professores_l_diverse ORDER BY genero, idade, salario
    );
""")