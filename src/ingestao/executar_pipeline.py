"""Orquestrador do Pipeline E1: Migracoes -> Bronze (Multi-Fontes) -> OLTP (3FN).

Executa em sequencia estrita e de forma idempotente:
1. Migracoes SQL (src/db/migrar.py);
2. Carga Bronze do CAGED (src/ingestao/carga_bronze.py);
3. Carga Bronze do IBGE (src/ingestao/carga_ibge.py);
4. Carga Bronze da CBO (src/ingestao/carga_cbo.py);
5. Transformacao e normalizacao para o modelo relacional 3FN (src/ingestao/carga_oltp.py).
"""

import logging
import os
import sys
import time
from pathlib import Path

import psycopg

from src.db import migrar
from src.ingestao import carga_bronze, carga_cbo, carga_ibge, carga_oltp

log = logging.getLogger("pipeline")


def main() -> None:
    inicio = time.monotonic()
    log.info("=== 1. Aplicando Migracoes SQL (0001, 0002, 0003) ===")
    migrar.main()

    log.info("=== 2. Carga Bronze: Microdados CAGED (MTE) ===")
    carga_bronze.main([])

    log.info("=== 3. Carga Bronze: IBGE Localidades e CNAE Subclasses ===")
    carga_ibge.main()

    log.info("=== 4. Carga Bronze: Classificacao CBO 2002 (MTE) ===")
    carga_cbo.main()

    log.info("=== 5. Transformacao e Carga para Modelo Relacional OLTP 3FN ===")
    with psycopg.connect(autocommit=True) as conn:
        carga_oltp.popular_municipios(conn)
        carga_oltp.popular_cnae(conn)
        carga_oltp.popular_cbo(conn)
        # Por padrao em execucao completa, carrega as movimentacoes
        carga_oltp.popular_movimentacoes(conn)

    duracao = time.monotonic() - inicio
    log.info("=== Pipeline E1 executado com sucesso em %.2fs ===", duracao)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
