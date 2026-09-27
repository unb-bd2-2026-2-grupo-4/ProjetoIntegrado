-- 0002 - Modelagem Transacional (3FN) do Novo CAGED
--
-- Esta migração cria o modelo relacional de produção (OLTP) que simularemos,
-- aplicando restrições reais de integridade (tipos estritos, PKs, FKs, NOT NULL).

CREATE SCHEMA IF NOT EXISTS oltp;

COMMENT ON SCHEMA oltp IS
    'Banco transacional relacional modelado em 3FN, simulando a origem dos dados do CAGED.';

-- Tabela Domínio: Município
CREATE TABLE oltp.municipio (
    id_municipio CHAR(7) PRIMARY KEY,
    sigla_uf     CHAR(2) NOT NULL
);

-- Tabela Domínio: Classificação Brasileira de Ocupações (CBO 2002)
CREATE TABLE oltp.cbo_2002 (
    codigo CHAR(6) PRIMARY KEY
);

-- Tabela Domínio: CNAE (Secao)
CREATE TABLE oltp.cnae_secao (
    codigo CHAR(1) PRIMARY KEY
);

-- Tabela Domínio: CNAE (Subclasse)
CREATE TABLE oltp.cnae_subclasse (
    codigo CHAR(7) PRIMARY KEY,
    codigo_secao CHAR(1) NOT NULL REFERENCES oltp.cnae_secao (codigo)
);

-- Tabela Principal (Movimentações)
CREATE TABLE oltp.movimentacao (
    id_movimentacao    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ano                INTEGER NOT NULL CHECK (ano >= 2020),
    mes                INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    id_municipio       CHAR(7) NOT NULL REFERENCES oltp.municipio (id_municipio),
    cnae_2_subclasse   CHAR(7) NOT NULL REFERENCES oltp.cnae_subclasse (codigo),
    cbo_2002           CHAR(6) NOT NULL REFERENCES oltp.cbo_2002 (codigo),
    
    -- Demografia
    sexo               INTEGER NOT NULL,
    raca_cor           INTEGER NOT NULL,
    idade              INTEGER NOT NULL CHECK (idade >= 14),
    grau_instrucao     INTEGER NOT NULL,
    
    -- Movimentação
    tipo_movimentacao  INTEGER NOT NULL,
    saldo_movimentacao INTEGER NOT NULL,
    
    -- Remuneração
    salario_mensal     NUMERIC(12, 2) NOT NULL,
    horas_contratuais  INTEGER NOT NULL,

    registrado_em      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE oltp.movimentacao IS
    'Tabela transacional com as movimentações reais de admissão e demissão.';
