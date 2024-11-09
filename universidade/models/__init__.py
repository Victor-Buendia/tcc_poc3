import os

from models.BaseModel import BaseModel
from models.docentes.Docente import Docente
from models.disciplinas.Disciplina import Disciplina
from models.discentes.Discente import Discente
from models.matriculadisciplinas.MatriculaDisciplina import MatriculaDisciplina

models = [
    (
        Docente, 
        int(os.environ.get('N_DOCENTES'))//int(os.environ.get('PROCESSES_NO'))
    ), 
    (
        Disciplina,
        int(os.environ.get('N_DISCIPLINAS'))//int(os.environ.get('PROCESSES_NO'))
    ),
    (
        Discente,
        int(os.environ.get('N_DISCENTES'))//int(os.environ.get('PROCESSES_NO'))
    ),
    (
        MatriculaDisciplina,
        int(os.environ.get('N_MATRICULAS'))//int(os.environ.get('PROCESSES_NO'))
    )
]
