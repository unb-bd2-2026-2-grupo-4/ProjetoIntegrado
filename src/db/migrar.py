"""Aplica, em ordem, as migrações SQL de src/db/migracoes ainda não aplicadas.

A conexão usa as variáveis padrão do libpq (PGHOST, PGPORT, PGDATABASE,
PGUSER, PGPASSWORD). Cada migração roda em uma transação própria e fica
registrada em public.schema_migracoes, então rodar de novo não faz nada.
"""

import logging
from pathlib import Path

import psycopg

DIRETORIO_MIGRACOES = Path(__file__).resolve().parent / "migracoes"

log = logging.getLogger("migrar")


def main() -> None:
    with psycopg.connect(autocommit=True) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS public.schema_migracoes (
                versao      TEXT PRIMARY KEY,
                aplicada_em TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
        aplicadas = {versao for (versao,) in conn.execute("SELECT versao FROM public.schema_migracoes")}

        for arquivo in sorted(DIRETORIO_MIGRACOES.glob("*.sql")):
            if arquivo.name in aplicadas:
                continue
            log.info("aplicando %s", arquivo.name)
            with conn.transaction():
                conn.execute(arquivo.read_text(encoding="utf-8"))
                conn.execute("INSERT INTO public.schema_migracoes (versao) VALUES (%s)", (arquivo.name,))

        log.info("banco atualizado")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    main()
