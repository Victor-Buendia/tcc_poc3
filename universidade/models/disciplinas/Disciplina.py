from datetime import datetime
from models.BaseModel import *
from . import *

class Disciplina(BaseModel):
    def __init__(self, **kwargs):
        nro_docentes = list(range(1, int(os.environ.get('N_DOCENTES'))))

        id_disciplina                           = 1 # Se generará com SQL usando ROW_NUMBER()
        nome_disciplina, curso                  = fake.random_element(elements=disciplinas)
        codigo_disciplina                       = f"{curso[:3].upper()}{fake.numerify(text='%%%')}"
        carga_horaria                           = fake.random_element(elements=[30, 45, 60, 90])
        matricula_docente                       = fake.random_element(elements=nro_docentes)
        status                                  = fake.random_element(elements=('Em Curso', 'Concluída', 'Cancelada'))

        kwargs.setdefault('id_disciplina',              id_disciplina)
        kwargs.setdefault('nome_disciplina',            nome_disciplina)
        kwargs.setdefault('curso',                      curso)
        kwargs.setdefault('codigo_disciplina',          codigo_disciplina)
        kwargs.setdefault('carga_horaria',              carga_horaria)
        kwargs.setdefault('matricula_docente',          matricula_docente)
        kwargs.setdefault('status',                     status)
        
        super().__init__(**kwargs)