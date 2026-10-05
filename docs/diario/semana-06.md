# Diário de Bordo - Semana 06

- **Data:** Semana 6 (Semestre 2026/2)
- **Autor(es):** Squad G4 (Arthur Evangelista, Davi Camilo, Eduardo de Pina, Euller Júlio, Lucas Alves, Tiago Antunes, Yan Matheus)

---

## O que foi medido e analisado

- **Documentação da Camada Bronze:** Estruturação da página técnica da camada bronze, formalizando o armazenamento dos dados brutos no PostgreSQL (schema `bronze`), as regras de linhagem até a linha de arquivo, atomicidade e idempotência baseada em hash SHA-256 para múltiplas fontes (Novo CAGED, IBGE e CBO).
- **Formalização do ADR 0001:** Redação e consolidação do registro de decisão de arquitetura sobre a modelagem transacional da origem (OLTP), avaliando detalhadamente a escolha de normalização em 3FN e do padrão estritamente *insert-only* frente às abordagens CRUD com sobrescrita e modelos desnormalizados *flat*.
- **Apresentação e defesa da Entrega 1 (E1):** Demonstração prática do ambiente do METRA funcionando via Docker Compose a partir de banco vazio, evidenciando integridade referencial, cargas automatizadas e a estratégia de reprodutibilidade com amostra representativa de dados.
- **Estrutura relacional do sistema de origem:** Avaliação dos relacionamentos entre a tabela de movimentações e as entidades dimensionais de apoio (localidades e ocupações) sob a ótica de integridade referencial.

## O que surpreendeu

- **Validação e aprovação da Entrega 1 (E1):** A entrega foi validada positivamente pela professora, que confirmou a consistência conceitual da abordagem adotada, a clareza da documentação e a eficácia da carga reprodutível.
- **Recomendação do Dagster como alternativa ao Airflow:** A professora reiterou a necessidade de evitar o excesso de complexidade de infraestrutura e apontou o Dagster como uma alternativa superior e mais enxuta em relação ao Apache Airflow, destacando seu paradigma moderno centrado em ativos de dados (*asset-based*) com menor pegada operacional para contêineres locais.
- **Apontamentos para o aprimoramento do MER:** A devolutiva da professora destacou a necessidade de ajustar o Modelo Entidade-Relacionamento (MER) para deixar evidente que o CAGED atua como a entidade/tabela principal do modelo transacional, centralizando as movimentações e recebendo explicitamente as múltiplas chaves estrangeiras provenientes das tabelas de referência do IBGE e da CBO.

## O que foi decidido

- **Homologação da Entrega 1:** Registro do cumprimento dos marcos da E1 com sucesso e consolidação da base de código no repositório oficial.
- **Refinamento do Modelo Entidade-Relacionamento (MER):** Adequação formal do modelo relacional para posicionar o CAGED de forma inequívoca como a tabela principal transacional, receptora direta das chaves estrangeiras vinculadas aos municípios (IBGE) e às ocupações (CBO 2002), reforçando a clareza conceitual da modelagem.
- **Adoção preferencial do Dagster para orquestração:** Priorização do estudo e incorporação do Dagster em substituição ao Apache Airflow, atendendo diretamente à recomendação de manter a infraestrutura simplificada e aderente aos fluxos de engenharia de dados.
- **Continuidade do estudo de banco de dados vetorial:** Manter o planejamento da integração vetorial alinhado às diretrizes pedagógicas, assegurando que sua adoção ocorra de maneira enxuta (como extensão relacional vetorial) para não reintroduzir sobrecarga desnecessária na arquitetura.
