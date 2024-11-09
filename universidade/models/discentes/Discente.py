from models.BaseModel import *
from . import *

class Discente(BaseModel):
    def __init__(self, **kwargs):

        matricula       = 1 # Se generará com SQL usando ROW_NUMBER()
        genero          = fake.random_element(elements=('Masculino', 'Feminino')) if random.random() <= 0.7 else 'Outro'
        nome            = fake.name() if genero == 'Outro' else (fake.name_male() if genero == 'Masculino' else fake.name_female())
        while regex.match(pattern=r'^[(Dr)(Sr)]', string=nome):
            nome        = fake.name()
        cpf             = fake.cpf()
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=26).isoformat()
        semestre        = fake.random_int(min=1, max=12)
        nacionalidade   = fake.country_code() if random.random() < 0.2 else 'BR'
        telefone        = fake.cellphone_number()
        _, curso        = fake.random_element(elements=disciplinas)
        while regex.match(pattern=r'^.\d{2} \(\d{2}\) \d{5}-\d{4}$', string=telefone) == None:
            telefone    = fake.cellphone_number()
        email           = regex.sub(pattern=r'@example\....', repl=fake.random_element(elements=['@gmail.com', '@hotmail.com', '@yahoo.com', '@outlook.com']), string=fake.ascii_safe_email())
        senha           = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        kwargs.setdefault('matricula',                  matricula)
        kwargs.setdefault('nome',                       nome)
        kwargs.setdefault('cpf',                        cpf)
        kwargs.setdefault('data_nascimento',            data_nascimento)
        kwargs.setdefault('semestre',                   semestre)
        kwargs.setdefault('curso',                      curso)
        kwargs.setdefault('nacionalidade',              nacionalidade)
        kwargs.setdefault('genero',                     genero)
        kwargs.setdefault('telefone',                   telefone)
        kwargs.setdefault('email',                      email)
        kwargs.setdefault('senha',                      senha)

        super().__init__(**kwargs)
