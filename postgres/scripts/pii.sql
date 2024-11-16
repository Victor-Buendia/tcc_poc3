ATTACH '' AS psql (TYPE POSTGRES);
CREATE OR REPLACE TABLE psql.pii.discentes AS (
    SELECT
        matricula,
        nome,
        cpf,
        data_nascimento,
        telefone,
        email
    FROM psql.public.discentes
);

CREATE OR REPLACE TABLE psql.public.discentes AS (
    SELECT
        matricula,
        semestre,
        curso,
        nacionalidade,
        genero,
        senha
    FROM psql.public.discentes
);


CREATE OR REPLACE TABLE psql.pii.docentes AS (
    SELECT
        matricula,
        nome,
        cpf,
        data_nascimento,
        telefone,
        email
    FROM psql.public.docentes
);

CREATE OR REPLACE TABLE psql.public.docentes AS (
    SELECT
        matricula,
        salario,
        especializacao,
        curso,
        nacionalidade,
        genero,
        senha
    FROM psql.public.docentes
);
