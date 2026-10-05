# Política e Registro de Uso de IA

O uso de assistentes e agentes de IA nesta disciplina é **esperado, não apenas tolerado**. O princípio norteador é a **transparência e o entendimento real do raciocínio**, conforme estabelecido na [Política de Uso de IA](https://unb-bd2.github.io/PlanoEnsino/uso-de-ia/) oficial de Banco de Dados 2 (FCTE-UnB).

> *"Não há penalidade por usar. Há penalidade por não declarar e por não entender."*

---

## Onde é Utilizado e Declarado

- **Arquitetura e Decisões:** Apoio na exploração de tradeoffs técnicos, confronto de alternativas formais (CRUD vs. Insert-Only, 3FN vs. Flat) e levantamento de restrições de infraestrutura para os ADRs.
- **Implementação:** Construção de esquemas SQL versionados, scripts de automação, pipelines de ingestão e testes de integridade referencial.
- **Documentação:** Estruturação de páginas técnicas, diagramas conceituais (Mermaid) e relatórios no MkDocs.

---

## Registro de Entradas (AI-USAGE)

O arquivo [`AI-USAGE.md`](https://github.com/unb-bd2-2026-2-grupo-4/ProjetoIntegrado/blob/main/AI-USAGE.md) na raiz do repositório é o instrumento oficial de auditoria contínua da Squad. Abaixo constam os registros contemporâneos de todas as atividades:

### 2026-09-15 - Planejamento de Arquitetura, Estruturação da Documentação e Planilha Técnica
- **Ferramenta:** Antigravity (Google DeepMind)
- **Onde:** `AI-USAGE.md`, `README.md`, `docs/diario/` e documentação MkDocs.
- **O que foi pedido:** Guia na seleção da stack técnica adequada para o Novo CAGED, estruturação do repositório.
- **O que foi aproveitado:** A escolha da arquitetura leve baseada em PostgreSQL (OLTP), MinIO/Parquet (Lakehouse), DuckDB/dbt (OLAP) e Metabase (Consumo); as justificativas técnicas e de mitigação de riscos para a planilha; a configuração do site de documentação com MkDocs Material.
- **Como foi verificado:** Confrontação com os requisitos do [Plano de Ensino](https://unb-bd2.github.io/PlanoEnsino/) e regras das Entregas (E1 a E4), checagem das diretrizes de vocabulário do [CONTEXT.md](https://github.com/UnB-BD2/PlanoEnsino/blob/main/CONTEXT.md) e viabilidade de execução reproduzível via Docker em máquina comum.
- **Quem revisou:** Arthur Evangelista

### 2026-09-16 - Camada bronze: carga dos CSVs brutos do Novo CAGED no PostgreSQL
- **Ferramenta:** Claude Code (Anthropic, Claude Opus 5)
- **Onde:** `src/db/`, `src/ingestao/carga_bronze.py`, `docker/ingestao/Dockerfile`, `docker-compose.yml`, `requirements-pipeline.txt`, `.dockerignore`, `.env.example`, `docs/camada-bronze.md`, `docs/diario/semana-04.md`.
- **O que foi pedido:** Atuar como engenheiro de dados para consumir os CSVs de `data/` e montar a camada bronze (dados brutos) seguindo a arquitetura do METRA.
- **O que foi aproveitado:** Perfil dos CSVs feito com DuckDB; schema `bronze` com todas as colunas como `TEXT` e linhagem por arquivo e linha; migração versionada com um executor simples; carga via `COPY` idempotente (SHA-256) e atômica por arquivo; serviços `postgres` e `ingestao-bronze` no Compose; página de documentação com as medições e os achados para a próxima camada.
- **Como foi verificado:** Carga executada em PostgreSQL 16.2 local com os 14.753.112 registros (54 s). Contagens por arquivo e por ano, nulos, zeros à esquerda e CBOs de 5 dígitos conferidos contra o perfil do DuckDB. Reexecução confirmou a idempotência, inclusive com arquivo renomeado. Um arquivo com linha malformada confirmou o rollback sem carga parcial. O caminho via Docker Compose não foi executado na máquina de desenvolvimento, que não tem Docker.
- **Quem revisou:** Lucas

### 2026-09-27 - Camada Bronze Multi-Fontes (IBGE e CBO), Modelo 3FN Insert-Only e Reprodutibilidade E1
- **Ferramenta:** Antigravity (Google DeepMind)
- **Onde:** `src/db/migracoes/0002_camada_bronze_referencias.sql`, `src/db/migracoes/0003_modelo_transacional_oltp.sql`, `src/ingestao/carga_ibge.py`, `src/ingestao/carga_cbo.py`, `src/ingestao/carga_oltp.py`, `src/ingestao/executar_pipeline.py`, `data/caged_centro_oeste_amostra.csv`, `docker-compose.yml`, `docs/adr/0001-modelagem-sistema-origem.md`, `docs/camada-bronze.md`, `docs/arquitetura.md`, `README.md`.
- **O que foi pedido:** Integrar fontes de dados secundárias oficiais (IBGE Localidades, IBGE CNAE 2.0 e CBO 2002) para cumprir o critério de múltiplas fontes na E1, estruturar suas tabelas brutas na camada Bronze com idempotência e linhagem, implementar a normalização completa do modelo relacional transacional em 3FN com padrão estritamente *insert-only* e integridade referencial estrita para o Centro-Oeste (2023-2026), criar amostra representativa versionada de 2,8 MB para garantir reprodutibilidade sem passos manuais por terceiros, e documentar formalmente os três carimbos de tempo e a decisão no ADR 0001.
- **O que foi aproveitado:** Migração de tabelas bronze de referência; enriquecimento das tabelas de domínio do schema `oltp` (`municipio`, `cbo_2002`, `cnae_secao`, `cnae_subclasse`); rotina de transformação e carga idempotente Bronze -> OLTP 3FN com tratamento de outliers e reconciliação de chaves administrativas; unificação do orquestrador de pipeline no contêiner de ingestão; garantia de fallback automático para a amostra representativa de 49 mil linhas se os arquivos pesados de 828 MB não estiverem presentes; revisão ortográfica completa em português culto acentuado.
- **Como foi verificado:** Execução real em contêiner PostgreSQL 16 local no Docker, medição de tempo de carga (IBGE municípios 0,33s, CNAE 0,19s, CBO 0,25s), verificação de integridade referencial com junções SQL relacionais, teste de recuperação de linhagem de movimentações para o arquivo CSV físico de origem, teste de build do portal MkDocs e confirmação de idempotência.
- **Quem revisou:** Arthur Evangelista

### 2026-10-05 - Registro dos Diários de Bordo (Semanas 05 e 06), Feedback da E1 e Ajustes de Arquitetura
- **Ferramenta:** Antigravity (Google DeepMind)
- **Onde:** `docs/diario/semana-05.md`, `docs/diario/semana-06.md`, `mkdocs.yml`, `README.md`, `AI-USAGE.md`, `docs/uso-de-ia.md`.
- **O que foi pedido:** Estruturar e documentar de forma técnica e profissional as atividades das Semanas 05 e 06 nos diários de bordo, registrando os preparativos para a demonstração, o feedback da professora quanto ao excesso de complexidade acidental e sobrecarga de infraestrutura, a entrega e validação positiva da E1, a recomendação do Dagster em substituição ao Airflow, a avaliação de banco de dados vetorial e o aprimoramento do MER com o CAGED como entidade principal centralizando as chaves estrangeiras de IBGE e CBO.
- **O que foi aproveitado:** Redação dos diários de bordo seguindo estritamente as seções canônicas ("O que foi medido e analisado", "O que surpreendeu" e "O que foi decidido") sem inclusão de tabelas ou gráficos conforme instruído; síntese das diretrizes pedagógicas recebidas; atualização do menu de navegação do MkDocs Material e árvore do repositório no README; sincronização dos registros de transparência no uso de IA.
- **Como foi verificado:** Revisão do conteúdo técnico frente às orientações da disciplina e aos apontamentos da professora; verificação de links, coerência cronológica e observância à exigência de não inserção de tabelas ou gráficos nos diários.
- **Quem revisou:** Squad G4 (Arthur Evangelista, Yan Matheus)

### 2026-10-05 - Correção de código e criação de diagramas Mermaid
- **Ferramenta:** Antigravity (Google DeepMind)
- **Onde:** `docs/relacionamentos.md` e arquivos de código-fonte.
- **O que foi pedido:** Correção de bugs na implementação atual e auxílio na sintaxe para a criação de diagramas Mermaid.
- **O que foi aproveitado:** O código corrigido e a estrutura gerada para a visualização gráfica dos relacionamentos no diagrama.
- **Como foi verificado:** Validação do funcionamento do código corrigido e verificação da renderização do diagrama na documentação.
- **Quem revisou:** Euller Júlio
