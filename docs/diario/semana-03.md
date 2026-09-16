# Diário de Bordo — Semana 03

- **Data:** Semana 3 (Semestre 2026/2)
- **Autor(es):** Squad G4 (Arthur Evangelista, Davi Camilo, Eduardo de Pina, Euller Júlio, Lucas Alves, Tiago Antunes, Yan Matheus)

---

## O que foi medido e analisado

- Mapeamento técnico detalhado para o preenchimento da **2ª Planilha de Acompanhamento** ("Engenharia de Dados aplicada ao seu projeto"), cobrindo os 5 blocos da apresentação teórica:
  1. *Fontes (Aba 1):* Microdados de Movimentações do CAGED, Microdados de Estabelecimentos do CAGED, Base Canônica de Municípios do IBGE e Tabela CBO 2002 de Ocupações.
  2. *Formatos (Aba 2):* Transição entre CSV bruto (landing zone), relacional 3FN (PostgreSQL operacional) e colunar compactado (Apache Parquet no MinIO).
  3. *Modelos (Aba 3):* Modelagem relacional transacional da origem versus modelo dimensional analítico (Star Schema com Fato Movimentações e tratamento de SCD Tipo 2).
  4. *Cargas e Engines (Aba 4):* PostgreSQL 16 para garantia ACID e escritas transacionais da E1 versus DuckDB para processamento analítico OLAP vetorizado em alta velocidade da E3.
  5. *Pipeline (Aba 5):* Da ingestão idempotente em lote e CDC (E2) às transformações dbt testadas (E3) e disponibilização dupla com ETL Reverso (E4).
- Levantamento de riscos de engenharia: saturação de memória RAM pelo volume bruto em contêineres locais, *schema drift* nas publicações mensais do MTE e requisitos de conformidade com a LGPD.

## O que surpreendeu

- A constatação de que soluções corporativas pesadas (como Apache Airflow ou Apache Spark) facilmente consomem mais de 4 GB de RAM apenas de overhead, o que colocaria em risco a execução limpa da plataforma em computadores convencionais de estudantes.
- A eficiência e maturidade do ecossistema moderno de dados local: a combinação de DuckDB + dbt-duckdb + MinIO local viabiliza executar consultas analíticas sobre milhões de linhas em frações de segundo com uso mínimo de CPU e memória.

## O que foi decidido

- **Preenchimento e entrega das 7 abas da 2ª Planilha** com justificativas técnicas centradas em critérios de engenharia e restrições não funcionais, e não apenas em nomes de ferramentas.
- **Definição preliminar da arquitetura da plataforma:**
  - Origem OLTP: PostgreSQL 16.
  - Armazenamento aberto: MinIO + Apache Parquet.
  - Motor analítico e modelagem: DuckDB + dbt-duckdb.
  - Visualização analítica: Metabase ou Apache Superset.
  - Orquestração: Dagster ou automação leve com agendamento declarativo.
- **Preparação da documentação base do repositório:** criação de `.gitignore`, `AI-USAGE.md`, histórico de diários e estruturação da pasta `docs/adr/` com o template do Método de Decisão para as próximas semanas.
