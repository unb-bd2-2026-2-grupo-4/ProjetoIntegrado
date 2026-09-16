# Plataforma de Dados do Mercado de Trabalho Formal (Novo CAGED)

Bem-vindo à documentação oficial da plataforma de dados desenvolvida pela **Squad G4** para a disciplina de **Banco de Dados 2** (Engenharia de Software — FCTE / Universidade de Brasília, Oferta 2026/2).

---

## A Squad

| Membro | Papel / Foco de Atuação |
|---|---|
| **Arthur Evangelista** | Engenharia de Dados & Modelagem Transacional (OLTP) |
| **Davi Camilo** | Engenharia de Dados & Ingestão / CDC |
| **Eduardo de Pina** | Armazenamento Analítico & Infraestrutura Docker |
| **Euller Júlio** | Modelagem Analítica & Transformações dbt |
| **Lucas Alves** | Qualidade de Dados & Orquestração |
| **Tiago Antunes** | Camada Semântica & ETL Reverso |
| **Yan Matheus** | Visualização de Dados & Governança / LGPD |

---

## Objetivo do Projeto Integrado

O **Projeto Integrado** costura os quatro módulos da disciplina: a construção de uma plataforma completa de engenharia de dados, partindo de uma fonte transacional (OLTP) modelada e populada a partir de dados públicos reais brasileiros até uma camada analítica de decisão com painéis gerenciais e **ETL reverso**.

Nosso domínio de estudo é o **Mercado de Trabalho Formal Brasileiro**, estruturado a partir dos microdados do **Novo CAGED** (Ministério do Trabalho e Emprego) e bases auxiliares do IBGE e CBO.

---

## Navegação Rápida

- **[Domínio e Gestão](dominio.md):** O problema da assimetria no emprego formal, as personas atendidas e as 5 perguntas de gestão.
- **[Arquitetura da Plataforma](arquitetura.md):** Visão técnica das quatro Entregas (E1 a E4) e a stack selecionada (PostgreSQL, MinIO, DuckDB, dbt, Metabase).
- **[Diário de Bordo](diario/semana-01.md):** Registros semanais sobre o que foi medido, o que surpreendeu e o que foi decidido.
- **[Decisões de Arquitetura (ADR)](adr/template.md):** Aplicação do Método de Decisão em 6 passos para as escolhas estruturais.
- **[Política de Uso de IA](uso-de-ia.md):** Registro transparente do uso de assistentes de IA conforme as diretrizes pedagógicas.
