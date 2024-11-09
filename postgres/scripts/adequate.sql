CREATE OR REPLACE TABLE disciplinas AS (
    SELECT DISTINCT
        (SELECT prof.matricula FROM docentes AS prof WHERE prof.curso = dis.curso ORDER BY RANDOM() LIMIT 1) AS matricula_docente,
        dis.* EXCLUDE(matricula_docente)
    FROM disciplinas AS dis
);

CREATE OR REPLACE TABLE disciplinas AS (
    SELECT DISTINCT *
    FROM disciplinas
    WHERE matricula_docente IS NOT NULL
);

CREATE OR REPLACE TABLE matriculadisciplinas AS (
    SELECT DISTINCT
        mat.id_matricula,
        dis.id_disciplina,
        dis.matricula_docente,
        mat.matricula_discente,
        mat.semestre,
        IF(dis.status = 'Em Curso', NULL, mat.nota) AS nota,
        IF(dis.status = 'Em Curso', NULL, mat.frequencia) AS frequencia,
        IF(dis.status = 'Em Curso', 'Cursando', mat.status) AS "status"
    FROM matriculadisciplinas AS mat
    JOIN disciplinas AS dis
        ON mat.id_disciplina = dis.id_disciplina
        AND dis.status in ('Em Curso', 'Concluída')
    JOIN discentes AS di
        ON mat.matricula_discente = di.matricula
        AND di.curso = dis.curso
);