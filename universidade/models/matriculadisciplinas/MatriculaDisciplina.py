from models.BaseModel import *
from . import *

class MatriculaDisciplina(BaseModel):
    def __init__(self, **kwargs):
        nro_docentes = list(range(1, int(os.environ.get('N_DOCENTES'))))
        nro_discentes = list(range(1, int(os.environ.get('N_DISCENTES'))))
        nro_disciplinas = list(range(1, int(os.environ.get('N_DISCIPLINAS'))))

        id_matricula                = 1 # Se generará com SQL usando ROW_NUMBER()
        matricula_discente          = fake.random_element(elements=nro_discentes)
        matricula_docente           = fake.random_element(elements=nro_docentes)
        id_disciplina               = fake.random_element(elements=nro_disciplinas)
        semestre                    = str('20'+str(fake.random_int(min=22, max=26))+'/'+str(fake.random_int(min=1, max=2)))
        nota                        = fake.random_int(min=5, max=10) if random.random() <= 0.7 else fake.random_int(min=0, max=10)
        frequencia                  = fake.random_int(min=75, max=100) if nota > 5 else fake.random_int(min=50, max=80)
        status                      = 'Aprovado' if (nota >= 5 and frequencia >= 75) else 'Reprovado'

        kwargs.setdefault('id_matricula',               id_matricula)
        kwargs.setdefault('matricula_discente',         matricula_discente)
        kwargs.setdefault('matricula_docente',          matricula_docente)
        kwargs.setdefault('id_disciplina',              id_disciplina)
        kwargs.setdefault('semestre',                   semestre)
        kwargs.setdefault('nota',                       nota)
        kwargs.setdefault('frequencia',                 frequencia)
        kwargs.setdefault('status',                     status)

        super().__init__(**kwargs)
