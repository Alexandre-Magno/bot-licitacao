
CREATE TABLE IF NOT EXISTS publicacoes (
    ano_compra int not null,
    sequencial_compra int not null,
    cnpj_orgao text not null,
    modalidade int not NULL,
    valor_total REAL not NULL,
    objeto text not NULL,
    dt_publicacao text not NULL,
    PRIMARY KEY (ano_compra,sequencial_compra,cnpj_orgao)
);

CREATE TABLE IF NOT EXISTS publicacoes_control (
    ano_compra int not null,
    sequencial_compra int not null,
    cnpj_orgao text not null,
    ANALISE_EDITAL boolean NULL,
    CHECK_PRAZO_ENTREGA boolean NULL,
    CHECK_HABILITACAO boolean NULL,
    upload_drive boolean NULL,
    PRIMARY KEY (ano_compra,sequencial_compra,cnpj_orgao)

)

