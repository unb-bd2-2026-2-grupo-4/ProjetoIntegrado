-- 0002 - Camada bronze de fontes de referencia (IBGE, CBO e CNAE)
--
-- A camada bronze preserva os dados brutos exatamente como recebidos das fontes oficiais
-- (APIs do IBGE e tabelas da CBO), sem normalizacao ou regras de negocio.
-- Essas tabelas fornecem a linhagem e o espelho das fontes secundarias exigidas pelo projeto.

CREATE SCHEMA IF NOT EXISTS bronze;

-- Espelho bruto da API de Localidades do IBGE (/api/v1/localidades/municipios)
CREATE TABLE IF NOT EXISTS bronze.ibge_municipio (
    id_ingestao          BIGINT NOT NULL REFERENCES bronze.ingestao_arquivo (id_ingestao),
    numero_linha         BIGINT NOT NULL,
    id_municipio         TEXT,
    nome_municipio       TEXT,
    microrregiao_id      TEXT,
    microrregiao_nome    TEXT,
    mesorregiao_id       TEXT,
    mesorregiao_nome     TEXT,
    uf_id                TEXT,
    uf_sigla             TEXT,
    uf_nome              TEXT,
    regiao_id            TEXT,
    regiao_sigla         TEXT,
    regiao_nome          TEXT,
    dados_brutos_json    JSONB,
    PRIMARY KEY (id_ingestao, numero_linha)
);

COMMENT ON TABLE bronze.ibge_municipio IS
    'Dados brutos de municipios da API oficial de Localidades do IBGE.';

-- Espelho bruto da tabela de ocupacoes CBO 2002 (Ministerio do Trabalho e Emprego)
CREATE TABLE IF NOT EXISTS bronze.cbo_ocupacao (
    id_ingestao          BIGINT NOT NULL REFERENCES bronze.ingestao_arquivo (id_ingestao),
    numero_linha         BIGINT NOT NULL,
    codigo               TEXT,
    titulo               TEXT,
    tipo                 TEXT,
    PRIMARY KEY (id_ingestao, numero_linha)
);

COMMENT ON TABLE bronze.cbo_ocupacao IS
    'Dados brutos de ocupacoes da Classificacao Brasileira de Ocupacoes (CBO 2002 - MTE).';

-- Espelho bruto da API de Estrutura CNAE Subclasses do IBGE (/api/v2/cnae/subclasses)
CREATE TABLE IF NOT EXISTS bronze.ibge_cnae_subclasse (
    id_ingestao          BIGINT NOT NULL REFERENCES bronze.ingestao_arquivo (id_ingestao),
    numero_linha         BIGINT NOT NULL,
    subclasse_id         TEXT,
    subclasse_descricao  TEXT,
    classe_id            TEXT,
    classe_descricao     TEXT,
    grupo_id             TEXT,
    grupo_descricao      TEXT,
    divisao_id           TEXT,
    divisao_descricao    TEXT,
    secao_id             TEXT,
    secao_descricao      TEXT,
    dados_brutos_json    JSONB,
    PRIMARY KEY (id_ingestao, numero_linha)
);

COMMENT ON TABLE bronze.ibge_cnae_subclasse IS
    'Dados brutos da classificacao de atividades economicas CNAE 2.0 Subclasses (IBGE).';
