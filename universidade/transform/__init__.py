import os
import json
import datetime

from libs import *

curated_path = os.environ.get('CURATED_PATH')
key = os.environ.get('AES_KEY_B64')
iv_b64 = os.environ.get('AES_IV_B64')

def calculate_age(birth_date):
    return (datetime.datetime.now() - datetime.datetime.strptime(birth_date, "%Y-%m-%d")).days // 365

encrypt = lambda data: encrypt_data_b64(key, iv_b64, data)

def transform_discentes(dir_name: str, file_path: str, thread_id: int) -> None:
    with open(file_path, 'r') as file:
        data = json.load(file)
        transformed_data = [
            {
                'id_discente': record['id_discente'],
                'nome': record['nome'],
                'primeiro_nome': record['nome'].split()[0],
                'cpf': record['cpf'],
                'masked_cpf': '*'*len(record['cpf'][:4]) + record['cpf'][4:-3] + '*'*len(record['cpf'][-3:]),
                'data_nascimento': record['data_nascimento'],
                'idade': calculate_age(record['data_nascimento']),
                'genero': record['genero'],
                'telefone': record['telefone'],
                'masked_telefone': '*'*(len(record['telefone'])-4) + str(record['telefone'][-4:]),
                'email': record['email'],
                'masked_email': '*'*(len(record['email'])-4) + record['email'].split('@')[0][-4:] + '@' + record['email'].split('@')[-1],
                'senha': hash_text(record['senha']),
                'token_cartao': hash_text(
                    json.dumps(
                        {
                        'numero': record['cartao']['numero'],
                        'nome': record['cartao']['nome'],
                        'bandeira': record['cartao']['bandeira'],
                        'validade': record['cartao']['validade'],
                        'cvv': record['cartao']['cvv'],
                        },
                        sort_keys=True
                    )
                ) if record['cartao'] else None,
                'masked_cartao': {
                    'numero': '*'*(len(record['cartao']['numero'])-4) + str(record['cartao']['numero'][-4:]),
                    'nome': record['cartao']['nome'],
                    'bandeira': record['cartao']['bandeira'],
                    'validade': record['cartao']['validade'],
                    'cvv': '*'*len(record['cartao']['cvv']),
                } if record['cartao'] else None,
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
    'discentes': no_transform,
    'matriculadisciplinas': no_transform,
}