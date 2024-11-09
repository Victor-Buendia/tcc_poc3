ATTACH '' AS psql (TYPE POSTGRES);
CREATE OR REPLACE TABLE psql.public.discentes AS (
    SELECT
        id_discente,
        primeiro_nome,
        masked_cpf AS cpf,
        idade,
        genero,
        masked_telefone AS telefone,
        masked_email AS email,
        token_cartao,
        senha,
    FROM psql.public.discentes
)