# AI-USAGE.md - Squad G4

Registro de uso de assistentes e agentes de IA no METRA - Monitoramento e Engenharia de dados do TRAbalho (Projeto Integrado).

Este arquivo cumpre a [Política de Uso de IA](https://unb-bd2.github.io/PlanoEnsino/uso-de-ia/)
da disciplina. Ele não é confissão nem formalidade: é o mesmo tipo de registro
que um ADR faz para decisões de arquitetura.

**Duas regras de forma.** Escreva **no momento do uso**, não na véspera da
Entrega: registro reconstruído de memória sai impreciso, e imprecisão aqui é o
que a política pune. E versione junto com o código: uma entrada por commit
relevante é melhor que um resumo mensal.

**Não precisa registrar** autocompletar de editor, correção ortográfica ou
tradução. Registre o que produziu artefato ou mudou uma decisão.

---

## Entradas

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
- **Como foi verificado:** Carga executada em PostgreSQL 16.2 local com os 14.753.112 registros (54 s). Contagens por arquivo e por ano, nulos, zeros à esquerda e CBOs de 5 dígitos conferidos contra o perfil do DuckDB. Reexecução confirmou a idempotência, inclusive com arquivo renomeado. Um arquivo com linha malformada confirmou o rollback sem carga parcial. O caminho via Docker Compose **não** foi executado na máquina de desenvolvimento, que não tem Docker.
- **Quem revisou:** _pendente_
