-- 0001 - Camada bronze do Novo CAGED
--
-- A bronze guarda o dado exatamente como veio da fonte: todas as colunas de
-- negócio são TEXT, sem conversão de tipo nem limpeza. Zeros à esquerda
-- (ex.: cnae_2_subclasse '0113000'), valores atípicos (ex.: salário 0.01) e
-- nulos são preservados; qualquer tratamento acontece nas camadas seguintes.

CREATE SCHEMA IF NOT EXISTS bronze;

COMMENT ON SCHEMA bronze IS
    'Dados brutos, imutáveis e append-only, com linhagem até o arquivo e a linha de origem.';

-- Um registro por arquivo carregado. O SHA-256 torna a carga idempotente:
-- o mesmo conteúdo nunca entra duas vezes, mesmo que o arquivo seja renomeado.
CREATE TABLE bronze.ingestao_arquivo (
    id_ingestao       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome_arquivo      TEXT        NOT NULL,
    sha256            CHAR(64)    NOT NULL UNIQUE CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    tamanho_bytes     BIGINT      NOT NULL CHECK (tamanho_bytes > 0),
    cabecalho         TEXT        NOT NULL,
    fonte             TEXT        NOT NULL,
    iniciado_em       TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- Preenchidos ao fim da carga, na mesma transação: uma linha visível
    -- (commitada) sempre tem os dois valores.
    linhas_carregadas BIGINT CHECK (linhas_carregadas >= 0),
    concluido_em      TIMESTAMPTZ,
    CHECK ((linhas_carregadas IS NULL) = (concluido_em IS NULL))
);

COMMENT ON TABLE bronze.ingestao_arquivo IS
    'Controle de cargas da bronze: um registro por arquivo bruto ingerido.';

-- Espelho 1:1 do CSV exportado de basedosdados.br_me_caged.microdados_movimentacao.
CREATE TABLE bronze.caged_movimentacao (
    id_ingestao        BIGINT NOT NULL REFERENCES bronze.ingestao_arquivo (id_ingestao),
    numero_linha       BIGINT NOT NULL CHECK (numero_linha >= 2),
    ano                TEXT,
    mes                TEXT,
    sigla_uf           TEXT,
    id_municipio       TEXT,
    cnae_2_secao       TEXT,
    cnae_2_subclasse   TEXT,
    cbo_2002           TEXT,
    sexo               TEXT,
    raca_cor           TEXT,
    idade              TEXT,
    grau_instrucao     TEXT,
    tipo_movimentacao  TEXT,
    saldo_movimentacao TEXT,
    salario_mensal     TEXT,
    horas_contratuais  TEXT,
    PRIMARY KEY (id_ingestao, numero_linha)
);

COMMENT ON TABLE bronze.caged_movimentacao IS
    'Microdados brutos de movimentação do Novo CAGED (Centro-Oeste), sem tratamento.';
COMMENT ON COLUMN bronze.caged_movimentacao.numero_linha IS
    'Linha física no arquivo de origem (o cabeçalho é a linha 1).';
