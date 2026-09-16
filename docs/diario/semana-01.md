# Diário de Bordo - Semana 01

- **Data:** Semana 1 (Semestre 2026/2)
- **Autor(es):** Squad G4 (Arthur Evangelista, Davi Camilo, Eduardo de Pina, Euller Júlio, Lucas Alves, Tiago Antunes, Yan Matheus)

---

## O que foi medido e analisado

- Análise detalhada do [Plano de Ensino](https://unb-bd2.github.io/PlanoEnsino/) e das regras do **Projeto Integrado** (55% da nota) e do portfólio de **ADRs** (15% da nota).
- Avaliação dos critérios da rubrica de correção das Entregas (E1 a E4), com destaque para os 30% atribuídos a **funcionamento e reprodutibilidade** a partir de um repositório público e de um `docker-compose.yml` que sobe do zero em máquina limpa.
- Mapeamento das competências dos membros da equipe em bancos de dados relacionais, modelagem de dados, Docker, Python e dados.

## O que surpreendeu

- A ênfase da disciplina em não utilizar datasets artificiais limpos: o objeto da disciplina é lidar com dados abertos governamentais reais, seus esquemas inconsistentes, problemas de codificação e séries temporais interrompidas.
- O aviso explícito sobre a armadilha mais cara da Semana 1: a escolha de um domínio que não tenha série temporal nem entidades que mudem de estado, o que inviabilizaria o CDC da E2 e as dimensões de variação lenta (SCD Tipo 2) da E3.
- O fato de que a reprodutibilidade é o critério eliminatório: código que só roda na máquina de quem desenvolveu é sumariamente desconsiderado.

## O que foi decidido

- **Formação oficial da Squad G4** com os 7 integrantes alinhados.
- Criação e inicialização do repositório Git público da Squad.
- Estabelecimento do compromisso de manter o `AI-USAGE.md` e o diário de bordo semanais contemporâneos às atividades desenvolvidas, sem deixar para a véspera das entregas.
