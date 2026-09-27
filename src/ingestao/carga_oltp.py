"""Transformacao e Carga do Modelo Transacional (OLTP em 3FN): Bronze -> OLTP.

Escopo do Projeto METRA:
- Regiao: Centro-Oeste (DF, GO, MT, MS);
- Periodo: 2023 a 2026.

Regras de normalizacao e integridade (3FN):
1. oltp.municipio: normalizado a partir de bronze.ibge_municipio com nomes oficiais,
   UFs e identificacao das capitais (Brasilia, Goiania, Cuiaba e Campo Grande).
2. oltp.cnae_secao e oltp.cnae_subclasse: normalizados a partir de bronze.ibge_cnae_subclasse.
3. oltp.cbo_2002: normalizado a partir de bronze.cbo_ocupacao (6 digitos).
4. oltp.movimentacao: fato operacional com tipos nativos (DATE, INTEGER, NUMERIC),
   chaves estrangeiras estritas para todas as entidades de dominio, checagens de integridade
   e linhagem para bronze.ingestao_arquivo (id_ingestao, numero_linha).
"""

import argparse
import logging
import sys
import time

import psycopg

log = logging.getLogger("carga_oltp")

CAPITAIS_CENTRO_OESTE = ("5300108", "5208707", "5103403", "5002704")


def popular_municipios(conn: psycopg.Connection) -> int:
    qtd = conn.execute("SELECT count(*) FROM oltp.municipio").fetchone()[0]
    if qtd >= 5500:
        log.info("oltp.municipio ja populado (%d registros), pulando.", qtd)
        return qtd

    log.info("Populando oltp.municipio a partir de bronze.ibge_municipio...")
    inicio = time.monotonic()
    with conn.transaction():
        # Popula municipios do IBGE
        resultado = conn.execute(
            """
            INSERT INTO oltp.municipio (id_municipio, nome, sigla_uf, nome_uf, regiao, is_capital)
            SELECT
                lpad(id_municipio, 7, '0') AS id_municipio,
                nome_municipio AS nome,
                uf_sigla AS sigla_uf,
                uf_nome AS nome_uf,
                regiao_nome AS regiao,
                CASE WHEN id_municipio = ANY(%s) THEN true ELSE false END AS is_capital
            FROM bronze.ibge_municipio
            WHERE id_municipio IS NOT NULL AND uf_sigla IS NOT NULL
            ON CONFLICT (id_municipio) DO UPDATE
            SET nome = EXCLUDED.nome,
                sigla_uf = EXCLUDED.sigla_uf,
                nome_uf = EXCLUDED.nome_uf,
                regiao = EXCLUDED.regiao,
                is_capital = EXCLUDED.is_capital;
            """,
            (list(CAPITAIS_CENTRO_OESTE),),
        )
        total = resultado.rowcount

        # Garante registro fallback caso haja registros sem municipio na origem
        conn.execute(
            """
            INSERT INTO oltp.municipio (id_municipio, nome, sigla_uf, nome_uf, regiao, is_capital)
            VALUES ('9999999', 'MUNICIPIO NAO IDENTIFICADO', 'NI', 'Nao Identificado', 'Centro-Oeste', false)
            ON CONFLICT (id_municipio) DO NOTHING;
            """
        )

    duracao = time.monotonic() - inicio
    log.info("oltp.municipio: %d registros em %.2fs", total, duracao)
    return total


def popular_cnae(conn: psycopg.Connection) -> None:
    qtd = conn.execute("SELECT count(*) FROM oltp.cnae_subclasse").fetchone()[0]
    if qtd >= 1334:
        log.info("oltp.cnae ja populado (%d registros), pulando.", qtd)
        return

    log.info("Populando oltp.cnae_secao e oltp.cnae_subclasse a partir de bronze.ibge_cnae_subclasse...")
    inicio = time.monotonic()
    with conn.transaction():
        # Secoes
        conn.execute(
            """
            INSERT INTO oltp.cnae_secao (codigo, descricao)
            SELECT DISTINCT
                secao_id AS codigo,
                secao_descricao AS descricao
            FROM bronze.ibge_cnae_subclasse
            WHERE secao_id IS NOT NULL
            ON CONFLICT (codigo) DO UPDATE SET descricao = EXCLUDED.descricao;

            INSERT INTO oltp.cnae_secao (codigo, descricao)
            VALUES ('Z', 'ATIVIDADES NAO IDENTIFICADAS OU NAO ESPECIFICADAS')
            ON CONFLICT (codigo) DO NOTHING;
            """
        )

        # Subclasses
        resultado = conn.execute(
            """
            INSERT INTO oltp.cnae_subclasse (codigo, descricao, codigo_secao)
            SELECT DISTINCT
                lpad(subclasse_id, 7, '0') AS codigo,
                subclasse_descricao AS descricao,
                secao_id AS codigo_secao
            FROM bronze.ibge_cnae_subclasse
            WHERE subclasse_id IS NOT NULL AND secao_id IS NOT NULL
            ON CONFLICT (codigo) DO UPDATE
            SET descricao = EXCLUDED.descricao,
                codigo_secao = EXCLUDED.codigo_secao;

            INSERT INTO oltp.cnae_subclasse (codigo, descricao, codigo_secao)
            VALUES ('9999999', 'ATIVIDADES ECONOMICAS NAO IDENTIFICADAS', 'Z')
            ON CONFLICT (codigo) DO NOTHING;

            -- Garante subclasses historicas ou administrativas do CAGED nao presentes na API atual
            INSERT INTO oltp.cnae_subclasse (codigo, descricao, codigo_secao)
            SELECT DISTINCT
                lpad(m.cnae_2_subclasse, 7, '0') AS codigo,
                'SUBCLASSE CNAE ' || lpad(m.cnae_2_subclasse, 7, '0') || ' (REGISTRO ADMINISTRATIVO)' AS descricao,
                COALESCE(NULLIF(m.cnae_2_secao, ''), 'Z') AS codigo_secao
            FROM bronze.caged_movimentacao m
            WHERE m.cnae_2_subclasse IS NOT NULL AND m.cnae_2_subclasse != ''
              AND NOT EXISTS (
                  SELECT 1 FROM oltp.cnae_subclasse c WHERE c.codigo = lpad(m.cnae_2_subclasse, 7, '0')
              )
            ON CONFLICT (codigo) DO NOTHING;
            """
        )
        total = conn.execute("SELECT count(*) FROM oltp.cnae_subclasse").fetchone()[0]

    duracao = time.monotonic() - inicio
    log.info("oltp.cnae: %d subclasses cadastradas em %.2fs", total, duracao)


def popular_cbo(conn: psycopg.Connection) -> None:
    qtd = conn.execute("SELECT count(*) FROM oltp.cbo_2002").fetchone()[0]
    if qtd >= 3000:
        log.info("oltp.cbo_2002 ja populado (%d registros), pulando.", qtd)
        return

    log.info("Populando oltp.cbo_2002 a partir de bronze.cbo_ocupacao...")
    inicio = time.monotonic()
    with conn.transaction():
        # Insere a partir da tabela CBO oficial
        conn.execute(
            """
            INSERT INTO oltp.cbo_2002 (codigo, titulo)
            SELECT
                lpad(replace(codigo, '-', ''), 6, '0') AS codigo,
                (array_agg(titulo ORDER BY CASE WHEN tipo = 'Ocupação' THEN 1 ELSE 2 END, length(titulo)))[1] AS titulo
            FROM bronze.cbo_ocupacao
            WHERE replace(codigo, '-', '') ~ '^[0-9]{4,6}$'
            GROUP BY 1
            ON CONFLICT (codigo) DO NOTHING;
            """
        )

        # Garante qualquer CBO recente ou atipico presente nas movimentacoes do CAGED
        conn.execute(
            """
            INSERT INTO oltp.cbo_2002 (codigo, titulo)
            SELECT DISTINCT
                lpad(m.cbo_2002, 6, '0') AS codigo,
                'OCUPACAO CBO ' || lpad(m.cbo_2002, 6, '0') || ' (ATUALIZACAO MTE)' AS titulo
            FROM bronze.caged_movimentacao m
            WHERE m.cbo_2002 IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM oltp.cbo_2002 c WHERE c.codigo = lpad(m.cbo_2002, 6, '0')
              )
            ON CONFLICT (codigo) DO NOTHING;
            """
        )

        (total,) = conn.execute("SELECT count(*) FROM oltp.cbo_2002").fetchone()

    duracao = time.monotonic() - inicio
    log.info("oltp.cbo_2002: %d ocupacoes cadastradas em %.2fs", total, duracao)


def popular_movimentacoes(conn: psycopg.Connection, limite: int | None = None) -> None:
    log.info(
        "Populando oltp.movimentacao a partir de bronze.caged_movimentacao (limite=%s)...",
        f"{limite:,}" if limite else "TOTAL",
    )
    inicio = time.monotonic()

    ordem_e_limite = f"ORDER BY m.id_ingestao, m.numero_linha LIMIT {limite}" if limite else ""

    with conn.transaction():
        resultado = conn.execute(
            f"""
            INSERT INTO oltp.movimentacao (
                ano, mes, id_municipio, cnae_2_subclasse, cbo_2002,
                sexo, raca_cor, idade, grau_instrucao,
                tipo_movimentacao, saldo_movimentacao,
                salario_mensal, horas_contratuais,
                id_ingestao, numero_linha
            )
            SELECT
                m.ano::integer,
                m.mes::integer,
                COALESCE(NULLIF(m.id_municipio, ''), '9999999'),
                COALESCE(NULLIF(lpad(m.cnae_2_subclasse, 7, '0'), ''), '9999999'),
                lpad(m.cbo_2002, 6, '0'),
                m.sexo::integer,
                m.raca_cor::integer,
                CASE 
                    WHEN m.idade IS NULL OR m.idade = '' THEN NULL
                    WHEN m.idade::integer BETWEEN 10 AND 120 THEN m.idade::integer
                    ELSE NULL
                END,
                m.grau_instrucao::integer,
                m.tipo_movimentacao::integer,
                m.saldo_movimentacao::integer,
                CASE 
                    WHEN m.salario_mensal IS NULL OR m.salario_mensal = '' THEN 0.00
                    WHEN m.salario_mensal::numeric < 0 THEN 0.00
                    ELSE m.salario_mensal::numeric(16, 2)
                END,
                CASE 
                    WHEN m.horas_contratuais IS NULL OR m.horas_contratuais = '' THEN 0.00
                    WHEN m.horas_contratuais::numeric < 0 THEN 0.00
                    ELSE m.horas_contratuais::numeric(5, 2)
                END,
                m.id_ingestao,
                m.numero_linha
            FROM bronze.caged_movimentacao m
            WHERE m.sigla_uf IN ('DF', 'GO', 'MT', 'MS')
              AND m.ano::integer BETWEEN 2023 AND 2026
            {ordem_e_limite}
            ON CONFLICT (id_ingestao, numero_linha) DO NOTHING;
            """
        )
        total = resultado.rowcount

    duracao = time.monotonic() - inicio
    taxa = total / duracao if duracao > 0 else 0
    log.info(
        "oltp.movimentacao: %s registros carregados em %.2fs (%s reg/s)",
        f"{total:,}",
        duracao,
        f"{taxa:,.0f}",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga Bronze -> OLTP 3FN (METRA)")
    parser.add_argument(
        "--limite-movimentacoes",
        type=int,
        default=None,
        help="Limite de registros de movimentacao para teste pontual (padrao: carrega tudo)",
    )
    parser.add_argument(
        "--apenas-dominios",
        action="store_true",
        help="Carrega apenas as tabelas de dominio (municipio, cbo, cnae)",
    )
    args = parser.parse_args()

    with psycopg.connect(autocommit=True) as conn:
        popular_municipios(conn)
        popular_cnae(conn)
        popular_cbo(conn)

        if not args.apenas_dominios:
            popular_movimentacoes(conn, limite=args.limite_movimentacoes)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
