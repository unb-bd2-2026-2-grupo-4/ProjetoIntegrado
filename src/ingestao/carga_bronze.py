"""Carga da camada bronze: CSVs brutos do Novo CAGED -> PostgreSQL (schema bronze).

Regras da bronze:
- o dado entra como veio: todas as colunas como TEXT, sem limpeza nem conversão
  (campo vazio no CSV vira NULL, que é como o BigQuery exporta nulos);
- cada linha guarda sua linhagem: o arquivo (id_ingestao) e a linha de origem;
- idempotente: um arquivo cujo SHA-256 já foi carregado é ignorado;
- atômica: cada arquivo entra em uma única transação, inteiro ou nada.

Uso:
    python src/ingestao/carga_bronze.py              # todos os *.csv de METRA_DATA_DIR
    python src/ingestao/carga_bronze.py arquivo.csv  # arquivos específicos

A conexão usa as variáveis padrão do libpq (PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD).
"""

import csv
import hashlib
import logging
import os
import sys
import time
from pathlib import Path

import psycopg

FONTE = "basedosdados.br_me_caged.microdados_movimentacao (export BigQuery, Centro-Oeste)"

COLUNAS = (
    "ano",
    "mes",
    "sigla_uf",
    "id_municipio",
    "cnae_2_secao",
    "cnae_2_subclasse",
    "cbo_2002",
    "sexo",
    "raca_cor",
    "idade",
    "grau_instrucao",
    "tipo_movimentacao",
    "saldo_movimentacao",
    "salario_mensal",
    "horas_contratuais",
)

DIRETORIO_PADRAO = Path(__file__).resolve().parents[2] / "data"
INTERVALO_LOG = 1_000_000

log = logging.getLogger("carga_bronze")


def calcular_sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def carregar_arquivo(conn: psycopg.Connection, caminho: Path) -> None:
    sha256 = calcular_sha256(caminho)

    ja_carregado = conn.execute(
        "SELECT id_ingestao, linhas_carregadas FROM bronze.ingestao_arquivo WHERE sha256 = %s",
        (sha256,),
    ).fetchone()
    if ja_carregado:
        log.info(
            "%s já carregado (id_ingestao=%s, %s linhas), ignorando",
            caminho.name, ja_carregado[0], ja_carregado[1],
        )
        return

    inicio = time.monotonic()
    with conn.transaction(), caminho.open(newline="", encoding="utf-8") as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor, None)
        if cabecalho is None or tuple(cabecalho) != COLUNAS:
            raise ValueError(f"{caminho.name}: cabeçalho inesperado {cabecalho}, esperado {list(COLUNAS)}")

        (id_ingestao,) = conn.execute(
            """
            INSERT INTO bronze.ingestao_arquivo (nome_arquivo, sha256, tamanho_bytes, cabecalho, fonte)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_ingestao
            """,
            (caminho.name, sha256, caminho.stat().st_size, ",".join(cabecalho), FONTE),
        ).fetchone()
        log.info("%s: iniciando carga (id_ingestao=%s)", caminho.name, id_ingestao)

        linhas = 0
        colunas_sql = ", ".join(("id_ingestao", "numero_linha") + COLUNAS)
        with conn.cursor().copy(f"COPY bronze.caged_movimentacao ({colunas_sql}) FROM STDIN") as copy:
            for campos in leitor:
                if not campos:  # linha em branco não carrega dado
                    continue
                if len(campos) != len(COLUNAS):
                    raise ValueError(
                        f"{caminho.name}: linha {leitor.line_num} tem {len(campos)} campos, esperado {len(COLUNAS)}"
                    )
                copy.write_row((id_ingestao, leitor.line_num, *[c if c != "" else None for c in campos]))
                linhas += 1
                if linhas % INTERVALO_LOG == 0:
                    log.info("%s: %s linhas enviadas", caminho.name, f"{linhas:,}")

        conn.execute(
            """
            UPDATE bronze.ingestao_arquivo
               SET linhas_carregadas = %s, concluido_em = clock_timestamp()
             WHERE id_ingestao = %s
            """,
            (linhas, id_ingestao),
        )

    duracao = time.monotonic() - inicio
    log.info(
        "%s: %s linhas carregadas em %.1fs (%s linhas/s)",
        caminho.name, f"{linhas:,}", duracao, f"{linhas / duracao:,.0f}",
    )


def main(argumentos: list) -> None:
    if argumentos:
        arquivos = [Path(a) for a in argumentos]
    else:
        diretorio = Path(os.environ.get("METRA_DATA_DIR", DIRETORIO_PADRAO))
        arquivos = sorted(diretorio.glob("*.csv"))
        if not arquivos:
            raise SystemExit(f"nenhum CSV encontrado em {diretorio}")

    with psycopg.connect(autocommit=True) as conn:
        for arquivo in arquivos:
            carregar_arquivo(conn, arquivo)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main(sys.argv[1:])
