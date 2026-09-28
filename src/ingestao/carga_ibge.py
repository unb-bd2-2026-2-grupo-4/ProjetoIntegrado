"""Carga da camada bronze: API de Localidades e CNAE do IBGE -> PostgreSQL (schema bronze).

Fontes:
- Municipios: https://servicodados.ibge.gov.br/api/v1/localidades/municipios
- Subclasses CNAE 2.0: https://servicodados.ibge.gov.br/api/v2/cnae/subclasses

Regras da bronze:
- Preserva dados brutos das respostas oficiais;
- Idempotente: calcula SHA-256 da resposta obtida e evita recargas desnecessarias;
- Armazena linhagem em bronze.ingestao_arquivo com timestamp e contagem de registros;
- Mantem o payload JSON completo na coluna dados_brutos_json para auditoria.
"""

import gzip
import hashlib
import json
import logging
import time
import urllib.request
from typing import Any

import psycopg

log = logging.getLogger("carga_ibge")

URL_MUNICIPIOS = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
URL_CNAE = "https://servicodados.ibge.gov.br/api/v2/cnae/subclasses"
USER_AGENT = "METRA-DataPipeline/1.0 (UnB BD2 Squad G4)"


def requisitar_json(url: str) -> tuple[bytes, list[dict[str, Any]]]:
    """Faz a requisicao HTTP tratando compressao gzip de forma transparente."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Encoding": "gzip",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        conteudo_bruto = resp.read()
        if resp.info().get("Content-Encoding") == "gzip" or conteudo_bruto[:2] == b"\x1f\x8b":
            conteudo_descompactado = gzip.decompress(conteudo_bruto)
        else:
            conteudo_descompactado = conteudo_bruto

    dados = json.loads(conteudo_descompactado.decode("utf-8"))
    return conteudo_descompactado, dados


def carregar_municipios(conn: psycopg.Connection) -> None:
    nome_arquivo = "ibge_municipios_api.json"
    log.info("Buscando dados de municipios na API do IBGE: %s", URL_MUNICIPIOS)
    conteudo_bytes, municipios = requisitar_json(URL_MUNICIPIOS)
    sha256 = hashlib.sha256(conteudo_bytes).hexdigest()

    ja_carregado = conn.execute(
        "SELECT id_ingestao, linhas_carregadas FROM bronze.ingestao_arquivo WHERE sha256 = %s",
        (sha256,),
    ).fetchone()
    if ja_carregado:
        log.info(
            "Municipios do IBGE ja carregados (id_ingestao=%s, %s registros), ignorando.",
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
                "id,nome,microrregiao,mesorregiao,UF,regiao",
                f"IBGE API Localidades ({URL_MUNICIPIOS})",
            ),
        ).fetchone()
        log.info("Registrada ingestao %s para municipios do IBGE", id_ingestao)

        linhas = 0
        colunas = (
            "id_ingestao, numero_linha, id_municipio, nome_municipio, "
            "microrregiao_id, microrregiao_nome, mesorregiao_id, mesorregiao_nome, "
            "uf_id, uf_sigla, uf_nome, regiao_id, regiao_sigla, regiao_nome, dados_brutos_json"
        )
        with conn.cursor().copy(f"COPY bronze.ibge_municipio ({colunas}) FROM STDIN") as copy:
            for idx, m in enumerate(municipios, start=1):
                micro = m.get("microrregiao") or {}
                meso = micro.get("mesorregiao") or {}
                uf = meso.get("UF") or (m.get("regiao-imediata") or {}).get("regiao-intermediaria", {}).get("UF") or {}
                regiao = uf.get("regiao") or {}

                copy.write_row((
                    id_ingestao,
                    idx,
                    str(m.get("id")),
                    m.get("nome"),
                    str(micro.get("id")) if micro.get("id") is not None else None,
                    micro.get("nome"),
                    str(meso.get("id")) if meso.get("id") is not None else None,
                    meso.get("nome"),
                    str(uf.get("id")) if uf.get("id") is not None else None,
                    uf.get("sigla"),
                    uf.get("nome"),
                    str(regiao.get("id")) if regiao.get("id") is not None else None,
                    regiao.get("sigla"),
                    regiao.get("nome"),
                    json.dumps(m, ensure_ascii=False),
                ))
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
    log.info("Municipios IBGE: %d registros carregados em %.2fs", linhas, duracao)


def carregar_cnae(conn: psycopg.Connection) -> None:
    nome_arquivo = "ibge_cnae_subclasses_api.json"
    log.info("Buscando dados de CNAE Subclasses na API do IBGE: %s", URL_CNAE)
    conteudo_bytes, subclasses = requisitar_json(URL_CNAE)
    sha256 = hashlib.sha256(conteudo_bytes).hexdigest()

    ja_carregado = conn.execute(
        "SELECT id_ingestao, linhas_carregadas FROM bronze.ingestao_arquivo WHERE sha256 = %s",
        (sha256,),
    ).fetchone()
    if ja_carregado:
        log.info(
            "CNAE Subclasses ja carregadas (id_ingestao=%s, %s registros), ignorando.",
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
                "subclasse,descricao,classe,grupo,divisao,secao",
                f"IBGE API CNAE ({URL_CNAE})",
            ),
        ).fetchone()
        log.info("Registrada ingestao %s para CNAE Subclasses", id_ingestao)

        linhas = 0
        colunas = (
            "id_ingestao, numero_linha, subclasse_id, subclasse_descricao, "
            "classe_id, classe_descricao, grupo_id, grupo_descricao, "
            "divisao_id, divisao_descricao, secao_id, secao_descricao, dados_brutos_json"
        )
        with conn.cursor().copy(f"COPY bronze.ibge_cnae_subclasse ({colunas}) FROM STDIN") as copy:
            for idx, sc in enumerate(subclasses, start=1):
                classe = sc.get("classe") or {}
                grupo = classe.get("grupo") or {}
                divisao = grupo.get("divisao") or {}
                secao = divisao.get("secao") or {}

                copy.write_row((
                    id_ingestao,
                    idx,
                    str(sc.get("id")),
                    sc.get("descricao"),
                    str(classe.get("id")) if classe.get("id") is not None else None,
                    classe.get("descricao"),
                    str(grupo.get("id")) if grupo.get("id") is not None else None,
                    grupo.get("descricao"),
                    str(divisao.get("id")) if divisao.get("id") is not None else None,
                    divisao.get("descricao"),
                    str(secao.get("id")) if secao.get("id") is not None else None,
                    secao.get("descricao"),
                    json.dumps(sc, ensure_ascii=False),
                ))
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
    log.info("CNAE Subclasses IBGE: %d registros carregados em %.2fs", linhas, duracao)


def main() -> None:
    with psycopg.connect(autocommit=True) as conn:
        carregar_municipios(conn)
        carregar_cnae(conn)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
