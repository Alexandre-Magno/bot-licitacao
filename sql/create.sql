
CREATE TABLE IF NOT EXISTS publicacoes (
    id SERIAL PRIMARY KEY,
    ano_compra int not null,
    sequencial_compra int not null,
    cnpj_orgao text not null,
    modalidade int not NULL,
    valor_total REAL not NULL,
    objeto text not NULL,
    dt_publicacao text not NULL
);