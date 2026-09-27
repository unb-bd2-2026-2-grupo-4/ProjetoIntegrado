"""Carga da camada bronze: Classificacao Brasileira de Ocupacoes (CBO 2002) -> PostgreSQL (schema bronze).

Fonte oficial padronizada:
- Repositorio Open Knowledge Brasil (datasets-br/cbo) derivado do Ministerio do Trabalho e Emprego (MTE).
- URL: https://raw.githubusercontent.com/datasets-br/cbo/master/data/lista.csv

Regras da bronze:
- Preserva o formato de entrada como texto (sem remocao de hifen ou formatacao forcada);
- Idempotente via SHA-256 e controle em bronze.ingestao_arquivo;
- Rastreabilidade por numero_linha e id_ingestao.
"""

import csv
import hashlib
import io
import logging
import time
import urllib.request

import psycopg

log = logging.getLogger("carga_cbo")

URL_CBO = "https://raw.githubusercontent.com/datasets-br/cbo/master/data/lista.csv"
USER_AGENT = "METRA-DataPipeline/1.0 (UnB BD2 Squad G4)"


def baixar_cbo(url: str) -> tuple[bytes, list[tuple[str, str, str]]]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        conteudo_bytes = resp.read()

    # O arquivo lista.csv esta codificado em latin1 ou utf-8
    try:
        texto = conteudo_bytes.decode("utf-8")
    except UnicodeDecodeError:
        texto = conteudo_bytes.decode("latin1")

    leitor = csv.reader(io.StringIO(texto))
    cabecalho = next(leitor, None)

    registros = []
    for linha in leitor:
        if len(linha) >= 2:
            codigo = linha[0].strip()
            termo = linha[1].strip()
            tipo = linha[2].strip() if len(linha) > 2 else "Ocupacao"
            registros.append((codigo, termo, tipo))

    return conteudo_bytes, registros


def carregar_cbo(conn: psycopg.Connection) -> None:
    nome_arquivo = "cbo_2002_lista.csv"
    log.info("Buscando dados de ocupacoes da CBO 2002 em: %s", URL_CBO)
    conteudo_bytes, registros = baixar_cbo(URL_CBO)
    sha256 = hashlib.sha256(conteudo_bytes).hexdigest()

    ja_carregado = conn.execute(
        "SELECT id_ingestao, linhas_carregadas FROM bronze.ingestao_arquivo WHERE sha256 = %s",
        (sha256,),
    ).fetchone()
    if ja_carregado:
        log.info(
            "CBO 2002 ja carregada (id_ingestao=%s, %s registros), ignorando.",
            ja_carregado[0],
            ja_carregado[1],
        )
        return

    inicio = time.monotonic()
    with conn.transaction():
        (id_ingestao,) = conn.execute(
            """
            INSERT INTO bronze.ingestao_arquivo (nome_arquivo, sha256, tamanho_bytes, cabecalho, fonte)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_ingestao
            """,
            (
                nome_arquivo,
                sha256,
                len(conteudo_bytes),
                "codigo,termo,tipo",
                f"CBO 2002 MTE ({URL_CBO})",
            ),
        ).fetchone()
        log.info("Registrada ingestao %s para CBO 2002", id_ingestao)

        linhas = 0
        colunas = "id_ingestao, numero_linha, codigo, titulo, tipo"
        with conn.cursor().copy(f"COPY bronze.cbo_ocupacao ({colunas}) FROM STDIN") as copy:
            for idx, (codigo, termo, tipo) in enumerate(registros, start=2):
                copy.write_row((id_ingestao, idx, codigo, termo, tipo))
                linhas += 1

        conn.execute(
            """
            UPDATE bronze.ingestao_arquivo
               SET linhas_carregadas = %s, concluido_em = clock_timestamp()
             WHERE id_ingestao = %s
            """,
            (linhas, id_ingestao),
        )

    duracao = time.monotonic() - inicio
    log.info("CBO 2002: %d registros carregados em %.2fs", linhas, duracao)


def main() -> None:
    with psycopg.connect(autocommit=True) as conn:
        carregar_cbo(conn)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
