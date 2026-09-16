# Diário de Bordo - Semana 03

- **Data:** Semana 3 (Semestre 2026/2)
- **Autor(es):** Squad G4 (Arthur Evangelista, Davi Camilo, Eduardo de Pina, Euller Júlio, Lucas Alves, Tiago Antunes, Yan Matheus)

---

## O que foi medido e analisado

- Mapeamento técnico detalhado para o preenchimento da **2ª Planilha de Acompanhamento** ("Engenharia de Dados aplicada ao seu projeto"), cobrindo os 5 blocos conceituais:
  1. *Fontes (Aba 1):* Fonte primária única: Cadastro Geral de Empregados e Desempregados (Novo CAGED), disponibilizado pela Base dos Dados (`br_me_caged`), contendo microdados de movimentações, movimentações fora do prazo e movimentações excluídas.
  2. *Formatos (Aba 2):* Transição entre CSV bruto (landing zone em `data/`), relacional 3FN (PostgreSQL operacional) e colunar compactado (Apache Parquet no MinIO).
  3. *Modelos (Aba 3):* Modelagem relacional transacional da origem (entidades de movimentações, estabelecimentos agregados, ocupações e perfil demográfico) versus modelo dimensional analítico (Star Schema com Fato Movimentações e tratamento de SCD Tipo 2).
  4. *Cargas e Engines (Aba 4):* PostgreSQL 16 para garantia ACID e escritas transacionais da E1 versus DuckDB para processamento analítico OLAP vetorizado em alta velocidade da E3.
  5. *Pipeline (Aba 5):* Da ingestão idempotente em lote e CDC (E2) às transformações dbt testadas (E3), com disponibilização dupla no Metabase e ETL Reverso de alertas (E4).
- Análise de restrições do conjunto de dados:
  - O Novo CAGED é desidentificado e não possui CPF nem CNPJ, exigindo modelagem baseada em perfis sociodemográficos e atributos de vínculo.
  - O cálculo do saldo oficial exige unificar movimentações regulares, adicionar movimentações fora do prazo e subtrair movimentações excluídas.
  - Presença de inconsistências conhecidas (valores atípicos de salários e códigos de município 99999 / UF 99).

## O que surpreendeu

- Ao avaliar a Pergunta de Gestão 3 ("Qual a diferença de saldo de empregos entre capitais e o interior?"), percebemos que um recorte restrito ao Distrito Federal impossibilitaria a resposta, pois o DF é uma unidade indivisível sem municípios de interior.
- O volume de dados: o Brasil inteiro gera mais de 60 milhões de registros em 3 anos, o que inviabilizaria a execução em computadores locais. A solução foi adotar a apenas a Região Centro-Oeste (DF, GO, MT, MS), que cobre a capital federal, capitais estaduais e municípios agroindustriais do interior, gerando um volume real de 15 a 16 milhões de linhas para os anos de 2023 a fevereiro de 2026.
- Limitação do BigQuery: ao tentar exportar o resultado completo de uma vez, a plataforma barrou a exportação por exceder o limite de 1 GB para arquivo único, exigindo a divisão da extração por anos (2023/2024 e 2025/2026 separadamente) para salvar no Google Drive.

## O que foi decidido

- **Preenchimento e entrega das abas da 2ª Planilha** com justificativas técnicas centradas em critérios de engenharia e restrições não funcionais.
- **Definição do recorte de dados:** Anos completos de 2023 a fevereiro de 2026 da Região Centro-Oeste (DF, GO, MT, MS) a partir do Novo CAGED, permitindo responder a todas as 5 perguntas de gestão.
- **Download dos microdados brutos:** Arquivos CSV de 2023 a 2026 extraídos via BigQuery e alocados na pasta local `data/` do projeto, protegidos pelo `.gitignore`.
- **Definição da arquitetura da plataforma METRA:**
  - Origem OLTP: PostgreSQL 16 com tabelas normalizadas e carga automatizada.
  - Armazenamento aberto: MinIO com Apache Parquet.
  - Motor analítico e modelagem: DuckDB com dbt-duckdb.
  - Visualização analítica: Metabase.

