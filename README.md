# METRA — Monitoramento e Engenharia de dados do TRAbalho

> **Plataforma de Dados do Mercado de Trabalho Formal (Novo CAGED)**  
> **Projeto Integrado — Banco de Dados 2 (FCTE / Universidade de Brasília)**  
> **Oferta:** 2026/2 | **Squad G4**

---

## Grupo

- **Arthur Evangelista**
- **Davi Camilo**
- **Eduardo de Pina**
- **Euller Júlio**
- **Lucas Alves**
- **Tiago Antunes**
- **Yan Matheus**

---

## Domínio e Problema

Pessoas que buscam emprego enfrentam grande assimetria de informação: é difícil saber com precisão quando e onde a contratação formal está aquecendo ou esfriando, e faltam evidências públicas consolidadas sobre disparidades salariais e de rotatividade por recorte sociodemográfico (gênero, raça/cor, idade, escolaridade). Atualmente, decisões críticas como _"é o momento adequado para buscar recolocação ou transição de carreira?"_ ou _"onde o poder público deve focar incentivos à geração de emprego?"_ ainda são tomadas baseadas em impressões empíricas (_feeling_).

O **METRA** constrói o pipeline completo de dados — do sistema transacional de origem à decisão analítica e operacional — para responder a perguntas de gestão fundamentadas sobre o mercado de trabalho formal brasileiro.

---

## Personas

1. **Trabalhador em busca de recolocação:** Busca entender tendências de contratação e demissão por setor econômico, dinâmica salarial e sazonalidade para planejar transições profissionais.
2. **Pesquisador e Gestor Público de Políticas de Emprego:** Necessita de subsídios estatísticos para avaliar dinâmicas regionais (capitais vs. interior), rotatividade setorial (_turnover_) e desigualdades sociodemográficas no emprego formal.

---

## Perguntas de Gestão

O **METRA** foi concebido para responder a cinco perguntas centrais:

1. **Qual setor econômico mais contratou e demitiu no Distrito Federal nos últimos 12 meses?**
2. **Existe sazonalidade evidente nas contratações e demissões (ex.: pico do comércio no fim de ano)?**
3. **Qual é a diferença no saldo líquido de empregos gerados entre as capitais e os municípios do interior?**
4. **Os setores com maior taxa de rotatividade (_turnover_) praticam salários médios mais baixos?**
5. **Como o perfil sociodemográfico (gênero, raça/cor, idade, escolaridade) impacta o nível salarial e as movimentações de admissão/desligamento?**

---

## Fontes de Dados

- **Principal:** [Novo CAGED — Microdados de Movimentação e Estabelecimentos](https://basedosdados.org/dataset/562b56a3-0b01-4735-a049-eeac5681f056?raw_data_source=59844eec-a948-4ef4-adf0-1db8228fc8e9) (Ministério do Trabalho e Emprego via _Base dos Dados_).
- **Auxiliares:**
  - **IBGE:** Tabela canônica de Municípios, Microrregiões e Regiões Metropolitanas.
  - **CBO 2002:** Classificação Brasileira de Ocupações (Ministério do Trabalho e Emprego).
  - **CNAE 2.0:** Classificação Nacional de Atividades Econômicas (Subclasses).

---

## Arquitetura e Roteiro de Entregas

O **METRA** é construído incrementalmente ao longo das quatro Entregas da disciplina, operando integralmente em contêineres Docker locais via `docker-compose.yml`:

```
[Dados Abertos: CAGED / IBGE / CBO]
                 │
                 ▼ (Carga Idempotente Versionada)
     ┌───────────────────────┐
E1   │   PostgreSQL 16       │  (Origem OLTP transacional em 3FN com histórico)
     └───────────┬───────────┘
                 │
                 ▼ (Ingestão em Lote e CDC via WAL)
     ┌───────────────────────┐
E2   │ MinIO + Apache Parquet│  (Armazenamento Analítico em Formato Aberto)
     └───────────┬───────────┘
                 │
                 ▼ (Processamento Vetorizado Multi-Core)
     ┌───────────────────────┐
E3   │ DuckDB + dbt-duckdb   │  (Modelagem Star Schema testada e orquestrada)
     └───────────┬───────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
 ┌─────────────┐   ┌──────────────────────────────┐
 │ Painel      │   │ Camada Semântica de Métricas │
 │ Analítico   │   │ + ETL Reverso de Alertas     │ E4
 │ (Metabase)  │   │ para Gestão Pública          │
 └─────────────┘   └──────────────────────────────┘
```

- **E1 (Semana 7):** Fonte transacional OLTP (PostgreSQL 16) modelada em 3FN, populada de forma reproduzível com dados reais de grande volume.
- **E2 (Semana 10):** Ingestão em lote e fluxo de captura contínua de mudanças (CDC) gravando em armazenamento aberto (MinIO + Parquet).
- **E3 (Semana 13):** Camada analítica transformada em modelo dimensional (Star Schema), com testes automatizados de qualidade via `dbt` e orquestração agendada.
- **E4 (Semana 16):** Camada dupla de consumo (dashboard analítico no Metabase + camada semântica de métricas), caminho de **ETL reverso** para retroalimentação da origem, linhagem de dados e conformidade com a LGPD.

---

## Estrutura do Repositório

```text
.
├── .github/
│   └── workflows/
│       └── deploy-docs.yml # Pipeline de deploy automatizado no GitHub Pages
├── .gitignore              # Regras de exclusão para dados locais, binários e ambientes
├── AI-USAGE.md             # Registro contemporâneo de uso de assistentes de IA (conforme política)
├── README.md               # Visão geral do METRA, domínio, setup e governança
├── docker-compose.yml      # Manifesto que sobe todos os serviços locais da plataforma (E1 a E4)
├── mkdocs.yml              # Configuração do portal de documentação (Material for MkDocs)
├── requirements-docs.txt   # Dependências Python para execução local do MkDocs
├── docker/                 # Arquivos de configuração e Dockerfiles dos serviços
├── src/                    # Scripts de ingestão, pipeline e transformações
├── data/                   # Diretório reservado para volumes locais (ignorado no git)
└── docs/
    ├── index.md            # Página inicial do site de documentação
    ├── dominio.md          # Detalhamento do domínio, personas e 5 perguntas de gestão
    ├── arquitetura.md      # Visão técnica das camadas e Entregas (E1 a E4)
    ├── uso-de-ia.md        # Política de transparência de IA
    ├── stylesheets/
    │   └── extra.css       # Estilização customizada com texto justificado
    ├── adr/                # Registros de Decisões de Arquitetura (Método de Decisão em 6 passos)
    │   └── template.md     # Template oficial Nygard padronizado para os ADRs
    └── diario/             # Diários de bordo semanais da Squad G4
        ├── semana-01.md    # Formação da Squad e alinhamento dos critérios de avaliação
        ├── semana-02.md    # Escolha do domínio, personas e as 5 perguntas de gestão
        └── semana-03.md    # Engenharia de Dados aplicada ao projeto e mapeamento de riscos
```

---

## Portal de Documentação (MkDocs)

Toda a documentação técnica do **METRA**, incluindo diários de bordo, justificativas de engenharia e decisões de arquitetura, está disponível em formato de portal web estruturado e com **texto justificado**.

### Como Rodar a Documentação Localmente

**Opção A — Via Docker Compose (Recomendado, sem instalar nada na máquina):**

```bash
docker compose up docs
```

Acesse no seu navegador: [http://localhost:8000](http://localhost:8000) (com recarregamento automático a cada alteração salva).

**Opção B — Via Python:**

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

---

## Como Subir o METRA (Ambiente Local)

### Pré-requisitos

- [Git](https://git-scm.com/)
- [Docker Engine](https://docs.docker.com/engine/) e [Docker Compose](https://docs.docker.com/compose/)

### Passos de Execução

```bash
# 1. Clonar o repositório público
git clone https://github.com/arthurevg/ProjetoIntegrado.git
cd ProjetoIntegrado

# 2. Subir a documentação localmente
docker compose up docs

# 3. Subir os serviços transacionais e analíticos do METRA (disponíveis a partir da E1)
# docker compose up -d
```

---

## Governança, Ética e Uso de IA

- **Uso de IA:** Este repositório cumpre integralmente a [Política de Uso de IA](https://unb-bd2.github.io/Disciplina/uso-de-ia/) da disciplina. Todas as contribuições de assistentes são documentadas de forma contemporânea no arquivo [`AI-USAGE.md`](./AI-USAGE.md).
- **ADRs:** Todas as decisões arquiteturais seguem o **Método de Decisão em 6 passos** e ficam versionadas em [`docs/adr/`](./docs/adr/).
- **Diário de Bordo:** O acompanhamento contínuo de aprendizados, medições e surpresas da Squad é registrado semanalmente em [`docs/diario/`](./docs/diario/).
