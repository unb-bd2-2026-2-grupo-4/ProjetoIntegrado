-- 0003 - Modelagem Transacional (3FN) do Sistema de Origem
--
-- Esta migracao cria o modelo relacional de producao (OLTP),
-- aplicando a 3FN com integridade referencial estrita (PKs, FKs, NOT NULL, CHECKs).
-- As entidades de dominio sao enriquecidas com os dados das fontes secundarias (IBGE e CBO).

CREATE SCHEMA IF NOT EXISTS oltp;

COMMENT ON SCHEMA oltp IS
    'Banco transacional relacional modelado em 3FN, simulando a origem dos dados do CAGED.';

-- Tabela Dominio: Municipio (Fonte primaria enriquecida via IBGE)
CREATE TABLE IF NOT EXISTS oltp.municipio (
    id_municipio CHAR(7) PRIMARY KEY,
    nome         VARCHAR(100) NOT NULL,
    sigla_uf     CHAR(2) NOT NULL,
    nome_uf      VARCHAR(50) NOT NULL,
    regiao       VARCHAR(20) NOT NULL,
    is_capital   BOOLEAN NOT NULL DEFAULT false
);

COMMENT ON TABLE oltp.municipio IS
    'Municipios oficiais do Brasil normalizados a partir dos dados do IBGE.';

-- Tabela Dominio: Secao da CNAE 2.0 (Fonte: IBGE)
CREATE TABLE IF NOT EXISTS oltp.cnae_secao (
    codigo    CHAR(1) PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL
);

COMMENT ON TABLE oltp.cnae_secao IS
    'Secoes da Classificacao Nacional de Atividades Economicas (CNAE 2.0).';

-- Tabela Dominio: Subclasse da CNAE 2.0 (Fonte: IBGE)
CREATE TABLE IF NOT EXISTS oltp.cnae_subclasse (
    codigo       CHAR(7) PRIMARY KEY,
    descricao    VARCHAR(255) NOT NULL,
    codigo_secao CHAR(1) NOT NULL REFERENCES oltp.cnae_secao (codigo)
);

COMMENT ON TABLE oltp.cnae_subclasse IS
    'Subclasses economicas da CNAE 2.0 vinculadas a secao correspondente.';

-- Tabela Dominio: Classificacao Brasileira de Ocupacoes (Fonte: CBO 2002 - MTE)
CREATE TABLE IF NOT EXISTS oltp.cbo_2002 (
    codigo CHAR(6) PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL
);

COMMENT ON TABLE oltp.cbo_2002 IS
    'Ocupacoes padronizadas pela Classificacao Brasileira de Ocupacoes (CBO 2002).';

-- Tabela Fato Transacional: Movimentacoes do CAGED
CREATE TABLE IF NOT EXISTS oltp.movimentacao (
    id_movimentacao    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ano                INTEGER NOT NULL CHECK (ano BETWEEN 2023 AND 2026),
    mes                INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    id_municipio       CHAR(7) NOT NULL REFERENCES oltp.municipio (id_municipio),
    cnae_2_subclasse   CHAR(7) NOT NULL REFERENCES oltp.cnae_subclasse (codigo),
    cbo_2002           CHAR(6) NOT NULL REFERENCES oltp.cbo_2002 (codigo),
    
    -- Demografia
    sexo               INTEGER NOT NULL CHECK (sexo IN (1, 3, 9)),
    raca_cor           INTEGER NOT NULL CHECK (raca_cor IN (1, 2, 3, 4, 5, 6, 9)),
    idade              INTEGER CHECK (idade IS NULL OR (idade >= 10 AND idade <= 120)),
    grau_instrucao     INTEGER NOT NULL,
    
    -- Movimentacao
    tipo_movimentacao  INTEGER NOT NULL,
    saldo_movimentacao INTEGER NOT NULL CHECK (saldo_movimentacao IN (-1, 1)),
    
    -- Remuneracao e Carga
    salario_mensal     NUMERIC(16, 2) CHECK (salario_mensal IS NULL OR salario_mensal >= 0),
    horas_contratuais  NUMERIC(5, 2) CHECK (horas_contratuais IS NULL OR horas_contratuais >= 0),

    -- Linhagem e rastreabilidade com a camada Bronze
    id_ingestao        BIGINT NOT NULL REFERENCES bronze.ingestao_arquivo (id_ingestao),
    numero_linha       BIGINT NOT NULL,
    registrado_em      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE oltp.movimentacao IS
    'Movimentacoes de admissao e desligamento em 3FN, com rastreabilidade a camada Bronze.';

-- Indices nas chaves estrangeiras para performance operacional
CREATE INDEX IF NOT EXISTS idx_oltp_movimentacao_municipio ON oltp.movimentacao (id_municipio);
CREATE INDEX IF NOT EXISTS idx_oltp_movimentacao_cbo ON oltp.movimentacao (cbo_2002);
CREATE INDEX IF NOT EXISTS idx_oltp_movimentacao_cnae ON oltp.movimentacao (cnae_2_subclasse);
CREATE INDEX IF NOT EXISTS idx_oltp_movimentacao_ano_mes ON oltp.movimentacao (ano, mes);
CREATE UNIQUE INDEX IF NOT EXISTS idx_oltp_movimentacao_origem ON oltp.movimentacao (id_ingestao, numero_linha);
