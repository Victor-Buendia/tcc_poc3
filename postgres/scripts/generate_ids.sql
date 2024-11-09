CREATE OR REPLACE TABLE disciplinas AS (
    SELECT DISTINCT
        ROW_NUMBER() OVER() AS id_disciplina,
        * EXCLUDE(id_disciplina)
    FROM disciplinas
);

CREATE OR REPLACE TABLE docentes AS (
    SELECT DISTINCT
        ROW_NUMBER() OVER() AS matricula,
        * EXCLUDE(matricula)
    FROM docentes
);

CREATE OR REPLACE TABLE discentes AS (
    SELECT DISTINCT
        ROW_NUMBER() OVER() AS matricula,
        * EXCLUDE(matricula)
    FROM discentes
);

CREATE OR REPLACE TABLE matriculadisciplinas AS (
    SELECT DISTINCT
        ROW_NUMBER() OVER() AS id_matricula,
        * EXCLUDE(id_matricula)
    FROM matriculadisciplinas
);