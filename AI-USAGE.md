# AI-USAGE.md — Squad G4

Registro de uso de assistentes e agentes de IA no METRA — Monitoramento e Engenharia de dados do TRAbalho (Projeto Integrado).

Este arquivo cumpre a [Política de Uso de IA](https://unb-bd2.github.io/Disciplina/uso-de-ia/)
da disciplina. Ele não é confissão nem formalidade: é o mesmo tipo de registro
que um ADR faz para decisões de arquitetura.

**Duas regras de forma.** Escreva **no momento do uso**, não na véspera da
Entrega — registro reconstruído de memória sai impreciso, e imprecisão aqui é o
que a política pune. E versione junto com o código: uma entrada por commit
relevante é melhor que um resumo mensal.

**Não precisa registrar** autocompletar de editor, correção ortográfica ou
tradução. Registre o que produziu artefato ou mudou uma decisão.

---

## Entradas

### 2026-09-15 — Planejamento de arquitetura, estruturação da documentação e preenchimento da planilha técnica de BD2

- **Ferramenta:** Antigravity (Google DeepMind)
- **Onde:** `AI-USAGE.md`, `README.md`, `docs/diario/`, planilha de acompanhamento de engenharia de dados (fontes, formatos, modelos, cargas e pipeline).
- **O que foi pedido:** Apoio na definição da stack técnica recomendada para o domínio do Novo CAGED, estruturação das respostas conceituais para a planilha pedagógica solicitada pela professora e organização do repositório em etapas com commits incrementais.
- **O que foi aproveitado:** A recomendação da stack baseada em PostgreSQL (OLTP), MinIO/Parquet (Lakehouse), DuckDB/dbt (OLAP) e Metabase/Superset; as justificativas técnicas para a planilha de acompanhamento; a organização do diário de bordo semanal e templates de documentação.
- **Como foi verificado:** Confrontação com o [Plano de Ensino](https://unb-bd2.github.io/Disciplina/) e regras das Entregas (E1 a E4), checagem das diretrizes de vocabulário (`CONTEXT.md`) e viabilidade de execução reproduzível em Docker Compose local limpo.
- **Quem revisou:** Arthur Evangelista
