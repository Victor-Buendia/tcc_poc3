import os
import json
import datetime

from libs import *

display_config()
public_key, private_key, relin_keys = generate_keypair()
set_public_key(public_key)
set_relin_keys(relin_keys)
display_config()

set_private_key(private_key)

display_config()

curated_path = os.environ.get('CURATED_PATH')
# key = os.environ.get('AES_KEY_B64')
# iv_b64 = os.environ.get('AES_IV_B64')

def calculate_age(birth_date):
    return (datetime.datetime.now() - datetime.datetime.strptime(birth_date, "%Y-%m-%d")).days // 365

# encrypt = lambda data: encrypt_data_b64(key, iv_b64, data)

def transform_discentes(dir_name: str, file_path: str, thread_id: int) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)
        transformed_data = [
            {
                'matricula': record['matricula'],
                'nome': record['nome'],
                'cpf': record['cpf'],
                'data_nascimento': record['data_nascimento'],
                'semestre': encrypt(record['semestre']).str_value,
                'curso': record['curso'],
                'nacionalidade': record['nacionalidade'],
                'genero': record['genero'],
                'telefone': record['telefone'],
                'email': record['email'],
                'senha': record['senha'],
                'token': generate_token(record['matricula']),
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
    'docentes': no_transform,
    'discentes': transform_discentes,
    'matriculadisciplinas': no_transform,
}