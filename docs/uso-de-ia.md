# Política e Registro de Uso de IA

O uso de assistentes e agentes de IA nesta disciplina é **esperado, não apenas tolerado**. O princípio norteador é a **transparência e o entendimento real do raciocínio**, conforme estabelecido na [Política de Uso de IA](https://unb-bd2.github.io/Disciplina/uso-de-ia/) oficial de Banco de Dados 2 (FCTE-UnB).

> *"Não há penalidade por usar. Há penalidade por não declarar e por não entender."*

---

## Onde é Utilizado e Declarado
- **Arquitetura e Decisões:** Apoio na exploração de tradeoffs técnicos, confronto de alternativas e levantamento de restrições de infraestrutura.
- **Implementação:** Construção de esquemas SQL, scripts de automação, pipelines de ingestão e testes.
- **Documentação:** Estruturação de páginas, diagramas conceituais e relatórios técnicos.

---

## Registro de Entradas (AI-USAGE)

O arquivo [`AI-USAGE.md`](https://github.com/arthurevg/ProjetoIntegrado/blob/main/AI-USAGE.md) na raiz do repositório é o instrumento oficial de auditoria contínua da Squad. Abaixo constam os registros contemporâneos das atividades:

### 2026-09-15 — Planejamento de Arquitetura, Estruturação da Documentação e Planilha Técnica
- **Ferramenta:** Antigravity (Google DeepMind)
- **Onde:** `AI-USAGE.md`, `README.md`, `docs/diario/`, documentação MkDocs e respostas da planilha de engenharia de dados.
- **O que foi pedido:** Apoio na seleção da stack técnica adequada para o Novo CAGED, estruturação conceitual da planilha pedagógica de BD2 e organização do repositório em etapas com commits incrementais.
- **O que foi aproveitado:** A escolha da arquitetura leve baseada em PostgreSQL (OLTP), MinIO/Parquet (Lakehouse), DuckDB/dbt (OLAP) e Metabase (Consumo); as justificativas técnicas e de mitigação de riscos para a planilha; a configuração do site de documentação com MkDocs Material.
- **Como foi verificado:** Confrontação com os requisitos do plano de ensino, checagem do vocabulário padronizado da disciplina (`CONTEXT.md`) e validação da viabilidade de execução reproduzível via Docker em máquina comum.
- **Quem revisou:** Arthur Evangelista
