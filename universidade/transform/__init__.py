import os
import json
import datetime

from libs import *

load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
display_config()

curated_path = os.environ.get('CURATED_PATH')
key = os.environ.get('AES_KEY_B64')
iv_b64 = os.environ.get('AES_IV_B64')

def calculate_age(birth_date):
    return (datetime.datetime.now() - datetime.datetime.strptime(birth_date, "%Y-%m-%d")).days // 365

encrypt_aes = lambda data: encrypt_data_b64(key, iv_b64, data)
encrypt_fhe = lambda data: encrypt(data).str_value

def transform_discentes(dir_name: str, file_path: str, thread_id: int) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)
        transformed_data = [
            {
                'matricula': record['matricula'],
                'nome': encrypt_aes(record['nome']),
                'cpf': encrypt_aes(record['cpf']),
                'data_nascimento': record['data_nascimento'],
                'semestre': record['semestre'],
                'curso': record['curso'],
                'nacionalidade': record['nacionalidade'],
                'genero': record['genero'],
                'telefone': encrypt_aes(record['telefone']),
                'email': encrypt_aes(record['email']),
                'senha': hash_text(record['senha']),
            } for record in data
        ]
    with open(curated_path.format(dir_name, dir_name, thread_id), 'w') as file:
        file.write(json.dumps(transformed_data))

def transform_docentes(dir_name: str, file_path: str, thread_id: int) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)
        transformed_data = [
            {
                'matricula': record['matricula'],
                'nome': encrypt_aes(record['nome']),
                'cpf': encrypt_aes(record['cpf']),
                'salario': encrypt_fhe(record['salario']),
                'data_nascimento': record['data_nascimento'],
                'especializacao': record['especializacao'],
                'curso': record['curso'],
                'nacionalidade': record['nacionalidade'],
                'genero': record['genero'],
                'telefone': encrypt_aes(record['telefone']),
                'email': encrypt_aes(record['email']),
                'senha': hash_text(record['senha']),
            } for record in data
        ]
    with open(curated_path.format(dir_name, dir_name, thread_id), 'w') as file:
        file.write(json.dumps(transformed_data))

def transform_matriculadisciplinas(dir_name: str, file_path: str, thread_id: int) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)
        transformed_data = [
            {
                'id_matricula': record['id_matricula'],
                'matricula_discente': record['matricula_discente'],
                'matricula_docente': record['matricula_docente'],
                'id_disciplina': record['id_disciplina'],
                'semestre': record['semestre'],
                'nota': encrypt_aes(record['nota']),
                'frequencia': record['frequencia'],
                'status': record['status'],
            } for record in data
        ]
    with open(curated_path.format(dir_name, dir_name, thread_id), 'w') as file:
        file.write(json.dumps(transformed_data))
        
def no_transform(dir_name: str, file_path: str, thread_id: int) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)
        transformed_data = [record for record in data]
    with open(curated_path.format(dir_name, dir_name[:-1], thread_id), 'w') as file:
        file.write(json.dumps(transformed_data))

transformation_mapping = {
    'disciplinas': no_transform,
    'docentes': transform_docentes,
    'discentes': transform_discentes,
    'matriculadisciplinas': transform_matriculadisciplinas,
}