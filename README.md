# METRA - Monitoramento e Engenharia de dados do TRAbalho

> **Plataforma de Dados do Mercado de Trabalho Formal (Novo CAGED)**  
> **Projeto Integrado: Banco de Dados 2 (FCTE / Universidade de Brasília)**  
> **Oferta:** 2026/2 | **Squad G4**

---

## Pergunta de Gestão Central (Entrega E1)

> **"Qual é a diferença no saldo líquido de empregos gerados e no salário médio de admissão entre as capitais e os municípios do interior da Região Centro-Oeste no período de 2023 a 2026?"**

---

## Grupo (Squad G4)

- **Arthur Evangelista**
- **Davi Camilo**
- **Eduardo de Pina**
- **Euller Júlio**
- **Lucas Alves**
- **Tiago Antunes**
- **Yan Matheus**

---

## Domínio e Problema

Pessoas que buscam emprego enfrentam grande assimetria de informação: é difícil saber com precisão quando e onde a contratação formal está aquecendo ou esfriando, e faltam evidências públicas consolidadas sobre disparidades salariais e de rotatividade por recorte sociodemográfico (gênero, raça/cor, idade, escolaridade). Decisões críticas como *"é o momento adequado para buscar recolocação ou transição de carreira?"* ou *"onde o poder público deve focar incentivos à geração de emprego?"* ainda são tomadas baseadas em impressões empíricas.

O **METRA** constrói o pipeline completo de dados, do sistema transacional de origem à decisão analítica e operacional, para responder a perguntas de gestão fundamentadas sobre o mercado de trabalho formal brasileiro no Centro-Oeste (DF, GO, MT, MS) entre 2023 e 2026.

---

## Personas

1. **Trabalhador em busca de recolocação:** Busca entender tendências de contratação e demissão por setor econômico, dinâmica salarial e sazonalidade para planejar transições profissionais.
2. **Pesquisador e Gestor Público de Políticas de Emprego:** Necessita de subsídios estatísticos para avaliar dinâmicas regionais (capitais vs. interior), rotatividade setorial (*turnover*) e desigualdades sociodemográficas no emprego formal.

---

## Perguntas de Gestão

O **METRA** foi concebido para responder a cinco perguntas centrais:

1. **Qual é a diferença no saldo líquido de empregos gerados e no salário médio entre as capitais e os municípios do interior?** (Pergunta Central E1)
2. **Qual setor econômico mais contratou e demitiu no Distrito Federal nos últimos 12 meses?**
3. **Existe sazonalidade evidente nas contratações e demissões (ex.: pico do comércio no fim de ano)?**
4. **Os setores com maior taxa de rotatividade (*turnover*) praticam salários médios mais baixos?**
5. **Como o perfil sociodemográfico (gênero, raça/cor, idade, escolaridade) impacta o nível salarial e as movimentações de admissão/desligamento?**

---

## Fontes Oficiais de Dados (Multi-Fontes)

O projeto integra três fontes públicas oficiais abertas:

1. **Novo CAGED (Ministério do Trabalho e Emprego):** [Microdados de Movimentação](https://basedosdados.org/dataset/562b56a3-0b01-4735-a049-eeac5681f056?raw_data_source=59844eec-a948-4ef4-adf0-1db8228fc8e9) contendo as declarações mensais obrigatórias de admissões e desligamentos formais (+14,7 milhões de linhas para o Centro-Oeste, 2023-2026, com amostra representativa versionada de 49 mil linhas para reprodutibilidade).
2. **IBGE (Instituto Brasileiro de Geografia e Estatística):**
   - **Localidades:** API REST oficial (`/api/v1/localidades/municipios`) fornecendo todos os 5.571 municípios brasileiros com microrregião, mesorregião, UF e região.
   - **CNAE 2.0 Subclasses:** API REST oficial (`/api/v2/cnae/subclasses`) com 1.332 subclasses econômicas e seções correspondentes.
3. **CBO 2002 (Ministério do Trabalho e Emprego):** Classificação Brasileira de Ocupações oficial com mais de 10 mil cargos formais e sinônimos ocupacionais.

---

## Arquitetura e Roteiro de Entregas

O **METRA** é construído incrementalmente ao longo das quatro Entregas da disciplina, operando integralmente em contêineres Docker locais via `docker-compose.yml`:

```text
[Fontes Oficiais: CAGED (MTE) / IBGE / CBO]
                 |
                 v (Carga Idempotente Versionada)
      +-----------------------+
E1    |   PostgreSQL 16       |  (Camada Bronze Raw + Schema OLTP 3FN Insert-Only)
      +-----------+-----------+
                  |
                  v (Ingestão em Lote e CDC via WAL)
      +-----------------------+
E2    | MinIO + Apache Parquet|  (Armazenamento Analítico em Formato Aberto)
      +-----------+-----------+
                  |
                  v (Processamento Vetorizado Multi-Core)
      +-----------------------+
E3    | DuckDB + dbt-duckdb   |  (Modelagem Star Schema testada e orquestrada)
      +-----------+-----------+
                  |
         +--------+--------+
         v                 v
  +-------------+   +------------------------------+
  | Painel      |   | Camada Semântica de Métricas |
  | Analítico   |   | + ETL Reverso de Alertas     | E4
  | (Metabase)  |   | para Gestão Pública          |
  +-------------+   +------------------------------+
```

- **E1 (Semana 7):** Camada Bronze multi-fontes e sistema transacional OLTP (PostgreSQL 16) modelado rigorosamente em 3FN com padrão *insert-only*, populado de forma reproduzível com dados reais de grande volume.
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
├── .gitignore              # Regras de exclusão para dados pesados (permite a amostra de 2.8 MB)
├── AI-USAGE.md             # Registro contemporâneo de uso de assistentes de IA (conforme política)
├── README.md               # Visão geral do METRA, domínio, setup e governança
├── docker-compose.yml      # Manifesto que sobe todos os serviços locais da plataforma (E1 a E4)
├── mkdocs.yml              # Configuração do portal de documentação (Material for MkDocs)
├── requirements-docs.txt   # Dependências Python para execução local do MkDocs
├── requirements-pipeline.txt # Dependências Python da ingestão e das migrações
├── .env.example            # Variáveis de ambiente do PostgreSQL (opcional)
├── docker/                 # Arquivos de configuração e Dockerfiles dos serviços
│   └── ingestao/Dockerfile # Imagem da tarefa de ingestão e carga do pipeline E1
├── src/                    # Scripts de ingestão, pipeline e transformações
│   ├── db/
│   │   ├── migrar.py       # Aplica migrações pendentes (registradas em public.schema_migracoes)
│   │   └── migracoes/      # Migrações SQL versionadas
│   │       ├── 0001_camada_bronze.sql             # Schema bronze inicial e microdados CAGED
│   │       ├── 0002_camada_bronze_referencias.sql # Tabelas bronze para IBGE e CBO
│   │       └── 0003_modelo_transacional_oltp.sql  # Schema OLTP normalizado em 3FN
│   └── ingestao/
│       ├── carga_bronze.py      # Carga dos CSVs do CAGED no schema bronze (com fallback automático)
│       ├── carga_ibge.py        # Ingestão das APIs do IBGE (municípios e CNAE) no bronze
│       ├── carga_cbo.py         # Ingestão da base CBO 2002 no bronze
│       ├── carga_oltp.py        # Promoção e normalização Bronze -> OLTP 3FN
│       └── executar_pipeline.py # Orquestrador sequencial de ponta a ponta
├── data/                   # Diretório de dados (inclui amostra versionada de 2.8 MB)
│   └── caged_centro_oeste_amostra.csv # Amostra representativa reproduzível (49.178 linhas)
└── docs/
    ├── index.md            # Página inicial do site de documentação
    ├── dominio.md          # Detalhamento do domínio, personas e 5 perguntas de gestão
    ├── arquitetura.md      # Visão técnica das camadas e Entregas (E1 a E4)
    ├── camada-bronze.md    # Regras, modelo multi-fontes e validações da camada bronze
    ├── uso-de-ia.md        # Política de transparência de IA
    ├── stylesheets/
    │   └── extra.css       # Estilização customizada com texto justificado
    ├── adr/                # Registros de Decisões de Arquitetura (Método de Decisão em 6 passos)
    │   ├── template.md     # Template oficial Nygard padronizado para os ADRs
    │   └── 0001-modelagem-sistema-origem.md # Decisão 3FN Insert-Only e multi-fontes
    └── diario/             # Diários de bordo semanais da Squad G4
        ├── semana-01.md    # Formação da Squad e alinhamento dos critérios de avaliação
        ├── semana-02.md    # Escolha do domínio, personas e as 5 perguntas de gestão
        ├── semana-03.md    # Engenharia de Dados aplicada ao projeto e mapeamento de riscos
        └── semana-04.md    # Perfil dos dados brutos e carga da camada bronze no PostgreSQL
```

---

## Como Subir o METRA (Execução 100% Reprodutível)

### Pré-requisitos

- [Git](https://git-scm.com/)
- [Docker Engine](https://docs.docker.com/engine/) e [Docker Compose](https://docs.docker.com/compose/)

### Passos de Execução

```bash
# 1. Clonar o repositório
git clone https://github.com/unb-bd2-2026-2-grupo-4/ProjetoIntegrado.git
cd ProjetoIntegrado

# 2. Subir a documentação localmente (opcional)
docker compose up -d docs

# 3. Subir o PostgreSQL 16
docker compose up -d postgres

# 4. Executar o pipeline E1 completo (migrações, bronze multi-fontes e modelo OLTP 3FN)
#    Se os CSVs pesados estiverem em data/, carrega os 14,7 milhões de registros.
#    Em uma máquina limpa de terceiro, utiliza automaticamente a amostra de 49 mil linhas versionada.
docker compose run --rm ingestao-bronze
```

Acesse o portal de documentação em: [http://localhost:8000](http://localhost:8000).

---

## Governança, Ética e Uso de IA

- **Uso de IA:** Este repositório cumpre integralmente a [Política de Uso de IA](https://unb-bd2.github.io/PlanoEnsino/uso-de-ia/) da disciplina. Todas as contribuições de assistentes são documentadas de forma contemporânea no arquivo [`AI-USAGE.md`](./AI-USAGE.md).
- **ADRs:** Todas as decisões arquiteturais seguem o **Método de Decisão em 6 passos** e ficam versionadas em [`docs/adr/`](./docs/adr/).
- **Diário de Bordo:** O acompanhamento contínuo de aprendizados, medições e surpresas da Squad é registrado semanalmente em [`docs/diario/`](./docs/diario/).
