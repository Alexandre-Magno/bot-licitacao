INSERT INTO publicacoes_control (ano_compra, sequencial_compra, cnpj_orgao)
select t1.ano_compra,t1.sequencial_compra,t1.cnpj_orgao from publicacoes t1
where not EXISTS (
select 1 from publicacoes_control t2
where t1.ano_compra = t2.ano_compra
AND t1.sequencial_compra = t2.sequencial_compra
AND t1.cnpj_orgao = t2.cnpj_orgao
)


