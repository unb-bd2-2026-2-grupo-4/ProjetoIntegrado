# Diário de Bordo - Semana 05

- **Data:** Semana 5 (Semestre 2026/2)
- **Autor(es):** Squad G4 (Arthur Evangelista, Davi Camilo, Euller Júlio, Lucas Alves, Tiago Antunes e Yan Matheus)

---

## O que foi medido e analisado

- **Preparativos para demonstração intermediária:** Planejamento e organização dos tópicos técnicos para a sessão de acompanhamento com a professora da disciplina, visando validar as premissas estruturais do projeto METRA.
- **Modelagem inicial da arquitetura da plataforma:** Elaboração da primeira proposta de arquitetura ponta a ponta para o METRA, contemplando os fluxos desde a ingestão dos dados abertos até as camadas analíticas e de visualização gerencial.
- **Avaliação da infraestrutura pretendida:** Levantamento dos requisitos operacionais e de recursos de máquina para sustentar múltiplos serviços e bancos de dados simultâneos no ecossistema local via contêineres.
- **Análise do acoplamento do fluxo de dados:** Identificação de desafios na coordenação e resolução de dependências entre as rotinas de ingestão, transformação e carga na ausência de um mecanismo unificado de orquestração.

## O que surpreendeu

- **Feedback docente sobre complexidade acidental:** Durante a apresentação da proposta de arquitetura, a professora pontuou que o desenho continha excesso de complexidade acidental e sobrecarga de infraestrutura, com serviços e camadas além do estritamente necessário para os objetivos do projeto.
- **Alerta sobre risco de sustentabilidade e foco:** O acúmulo desproporcional de infraestrutura eleva a barreira de reprodutibilidade em máquinas locais e desvia a atenção da equipe do núcleo da disciplina, que é o domínio de modelagem e engenharia de banco de dados.
- **Recomendações técnicas da professora:** Sugestão direta para simplificar a arquitetura global, incorporando formalmente um orquestrador de pipelines e avaliando a adoção de um banco de dados vetorial para expandir as capacidades de consulta e análise semântica.

## O que foi decidido

- **Simplificação arquitetural imediata:** Revisão da pilha da plataforma METRA para podar redundâncias operacionais e enxugar os componentes de infraestrutura, reduzindo a complexidade desnecessária.
- **Introdução de um orquestrador de dados:** Decisão de adotar uma ferramenta dedicada de orquestração para gerenciar o encadeamento, o monitoramento e a execução ordenada dos estágios de ingestão e transformação.
- **Estudo de viabilidade de banco de dados vetorial:** Abertura de uma frente de estudo para avaliar o uso de um banco de dados vetorial (como pgvector acoplado ao PostgreSQL ou alternativa equivalente leve), voltado a buscas por similaridade semântica de ocupações e enriquecimento do conjunto de dados.
- **Priorização dos artefatos da Entrega 1 (E1):** Concentrar esforços nos requisitos imediatos da E1 (modelagem relacional 3FN, integridade e carga da camada bronze), assegurando alinhamento aos critérios de avaliação antes de expandir novas camadas.
