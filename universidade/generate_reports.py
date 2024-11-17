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


### MÉDIA DE NOTA DE ALUNOS POR CURSO ###
disciplinas = conn.execute("SELECT * FROM psql.public.matriculadisciplinas").fetch_df()
# Etapa 1: Filtrar linhas com valores 'nota' NULL e carregar valores criptografados como bytes
media_notas = disciplinas[disciplinas['nota'].notnull()]
media_notas['nota'] = media_notas['nota'].apply(load_encrypted_str) # Carregar valores criptografados como bytes

# Etapa 2: Somar as notas por semestre ainda criptografadas em FHE
media_notas = media_notas.groupby('semestre')['nota'].apply(sum).apply(decrypt).reset_index() # Descriptografa a soma das notas
media_notas.columns = ['semestre', 'nota']

# Etapa 3: Calcular o número de alunos por semestre e calcular a média de 'nota'
media_notas['qtd_alunos'] = disciplinas.groupby('semestre').size().values
media_notas['media_notas'] = round(media_notas['nota'] / media_notas['qtd_alunos'], 2) # Calcula a média de notas

# Etapa 4: Remover colunas desnecessárias
media_notas_df = media_notas.drop(columns=['qtd_alunos', 'nota'])

# Etapa 5: Salvar no banco de dados
conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.media_notas_alunos AS (
        SELECT * FROM media_notas_df ORDER BY semestre ASC
    );
""")


### PUBLICAÇÃO DE INTERVALO DE SALÁRIOS POR GÊNERO ###
professores = conn.execute("SELECT D.*, P.data_nascimento FROM psql.public.docentes D JOIN psql.pii.docentes P ON D.matricula = P.matricula").fetch_df()

professores['salario'] = professores['salario'].apply(load_encrypted_str).apply(decrypt)
professores['idade'] = professores['data_nascimento'].apply(lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days // 365)
professores = professores.drop(columns=['senha', 'data_nascimento'])
conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.professores AS (
        SELECT * FROM professores ORDER BY matricula
    );
""")


publicacao_professores = conn.execute("SELECT D.*, P.data_nascimento FROM psql.public.docentes D JOIN psql.pii.docentes P ON D.matricula = P.matricula").fetch_df()

publicacao_professores['matricula'] = publicacao_professores['matricula'].apply(lambda x: generate_random_token(15))

publicacao_professores['idade'] = publicacao_professores['data_nascimento'].apply(lambda x: (pd.Timestamp.now() - pd.to_datetime(x)).days // 365)
publicacao_professores['idade'] = publicacao_professores['idade'].apply(lambda x: '> 40' if x > 40 else '<= 40')

publicacao_professores['salario'] = publicacao_professores['salario'].apply(load_encrypted_str).apply(decrypt)
publicacao_professores['salario'] = publicacao_professores['salario'].apply(lambda x: round(round(x/1000))*1000)

publicacao_professores = publicacao_professores.drop(columns=['nacionalidade', 'especializacao', 'data_nascimento', 'senha', 'curso'])

conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.professores_anonimizado AS (
        SELECT * FROM publicacao_professores ORDER BY genero, idade, salario
    );
""")


# Calcular L-Diversidade para o atributo sensível 'salario'
L = 2  # Defina o limiar L

# Etapa 1: Agrupar por quase-identificadores
grouped = publicacao_professores.groupby(['genero', 'idade'])

# Etapa 2: Calcular diversidade de 'salario' em cada grupo
diversity = grouped['salario'].nunique()

# Etapa 3: Identificar grupos que cumprem com L-diversidade
l_diverse = diversity >= L

# Etapa 4: Filtrar linhas que pertencem a grupos L-diversos
# Obter os grupos que atendem L-diversidade
conforming_groups = diversity[l_diverse].index

# Filtrar o DataFrame para grupos conformes
publicacao_professores_l_diversificado = publicacao_professores[
    publicacao_professores.set_index(['genero', 'idade']).index.isin(conforming_groups)
]

non_conforming_groups = diversity[~l_diverse]

conn.execute("""
    CREATE OR REPLACE TABLE psql.relatorios.publicacao_professores_l_diversificado AS (
        SELECT * FROM publicacao_professores_l_diversificado ORDER BY genero, idade, salario
    );
""")