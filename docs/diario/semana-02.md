# Diário de Bordo - Semana 02

- **Data:** Semana 2 (Semestre 2026/2)
- **Autor(es):** Squad G4 (Arthur Evangelista, Davi Camilo, Eduardo de Pina, Euller Júlio, Lucas Alves, Tiago Antunes, Yan Matheus)

---

## O que foi medido e analisado

- Exploração de fontes de dados abertos governamentais sugeridas pela disciplina:
  - Portal Brasileiro de Dados Abertos
  - SNIS (Sistema Nacional de Informações sobre Saneamento)
  - IBGE (portal de dados e malha de municípios)
  - Novo CAGED / MTE via Base dos Dados (conjunto `br_me_caged`)
- Verificação de volume e características temporais dos microdados do Novo CAGED:
  - Dezenas de milhões de registros anuais cobrindo admissões e desligamentos formais com carimbo temporal mensal.
  - Entidades com mudanças de estado ao longo do tempo (estabelecimentos que alteram porte/CNAE, trabalhadores que mudam de faixa salarial ou ocupação, fusões/mudanças cadastrais).
  - Presença de dados demográficos de interesse público (gênero, raça/cor, faixa etária, nível de instrução).

## O que surpreendeu

- A riqueza de variáveis no Novo CAGED possibilita cruzamentos analíticos profundos sobre dinâmicas econômicas e disparidades sociais no mercado de trabalho.
- O desafio técnico que o volume representará: baixar e carregar arquivos brutos sem filtro de escopo pode rapidamente saturar a memória da máquina local, exigindo recortes bem definidos (ex.: DF e capitais / períodos específicos para o ambiente de testes).
- A identificação precoce da persona consumidora para atender à exigência do **ETL reverso da E4**: não apenas gerar um gráfico passivo, mas devolver alertas de retração de vagas ou disparidades salariais para um gestor público de políticas de emprego.

## O que foi decidido

- **Definição do Domínio:** Mercado de Trabalho Formal Brasileiro (Novo CAGED via Base dos Dados / Ministério do Trabalho e Emprego).
- **Definição das Personas:**
  1. *Trabalhador em busca de recolocação:* Necessita de dados objetivos sobre tendências de contratação por setor, sazonalidade e remuneração real.
  2. *Pesquisador / Gestor Público:* Necessita de evidências empíricas sobre dinâmicas regionais (capitais vs. interior) e desigualdades no mercado de trabalho formal (gênero, raça/cor, idade, escolaridade).
- **Formulação das 5 Perguntas de Gestão:**
  1. Qual setor econômico mais contratou/demitiu no DF nos últimos 12 meses?
  2. Existe sazonalidade evidente nas contratações (ex.: aumento do comércio no fim de ano)?
  3. Qual a diferença de saldo líquido de postos entre capitais e o interior?
  4. Setores com maior rotatividade (*turnover*) praticam salários médios menores?
  5. Como o perfil sociodemográfico (gênero, raça/cor, idade, escolaridade) impacta os salários e a taxa de admissão/desligamento?
- **Entrega da 1ª Planilha** contendo a caracterização inicial da Squad G4 e do domínio escolhido.
