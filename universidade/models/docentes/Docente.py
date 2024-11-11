from models.BaseModel import *
from . import *

class Docente(BaseModel):
    def __init__(self, **kwargs):

        matricula               = 1 # Se generará com SQL usando ROW_NUMBER()
        genero                  = fake.random_element(elements=('Masculino', 'Feminino')) if random.random() <= 0.7 else 'Outro'
        nome                    = fake.name() if genero == 'Outro' else (fake.name_male() if genero == 'Masculino' else fake.name_female())
        if not regex.match(pattern=r'^[(Dr)(Sr)]', string=nome):
            nome                = 'Dr. ' + nome
        cpf                     = fake.cpf()
        data_nascimento         = fake.date_of_birth(minimum_age=30, maximum_age=70).isoformat()
        salario                 = fake.random_int(min=8_000, max=20_000)
        nacionalidade           = fake.country_code() if random.random() < 0.2 else 'BR'
        telefone                = fake.cellphone_number()
        especializacao, curso   = fake.random_element(elements=especializacoes)
        while regex.match(pattern=r'^.\d{2} \(\d{2}\) \d{5}-\d{4}$', string=telefone) == None:
            telefone            = fake.cellphone_number()
        email                   = regex.sub(pattern=r'@example\....', repl=fake.random_element(elements=['@gmail.com', '@hotmail.com', '@yahoo.com', '@outlook.com']), string=fake.ascii_safe_email())
        senha                   = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        kwargs.setdefault('matricula',                  matricula)
        kwargs.setdefault('nome',                       nome)
        kwargs.setdefault('cpf',                        cpf)
        kwargs.setdefault('salario',                    salario)
        kwargs.setdefault('data_nascimento',            data_nascimento)
        kwargs.setdefault('especializacao',             especializacao)
        kwargs.setdefault('curso',                      curso)
        kwargs.setdefault('nacionalidade',              nacionalidade)
        kwargs.setdefault('genero',                     genero)
        kwargs.setdefault('telefone',                   telefone)
        kwargs.setdefault('email',                      email)
        kwargs.setdefault('senha',                      senha)

        super().__init__(**kwargs)