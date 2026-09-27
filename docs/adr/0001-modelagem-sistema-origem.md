# 0001 - Modelagem do Sistema Transacional (Origem OLTP)

- **Status:** proposto
- **Data:** 2026-09-27
- **Decisores:** Euller Júlio e Squad G4

---

## 1. Contexto

Para a Entrega 1 (E1) do METRA, precisamos simular o banco de dados transacional de origem que alimentaria nosso Data Lake com os dados do Novo CAGED. 

**Caracterização da Carga de Trabalho:**
- **Volume:** Os microdados mensais do CAGED para o Centro-Oeste possuem milhões de linhas. A carga inicial importará o histórico (estimado em +5 milhões de registros).
- **Taxa de Escrita:** No mundo real (sistema em produção do MTE), inserções são massivas e ocorrem majoritariamente em lotes de atualizações das empresas (declarações mensais), com picos de `INSERT` no fim de cada mês.
- **Padrão de Acesso (Leitura):** Predominam leituras pontuais por chave para validar os dados do trabalhador e leituras por período para relatórios de fechamento.
- **Latência Tolerada:** Para a camada transacional de origem, inserções e validações de integridade precisam ocorrer em ms para não travar o envio das empresas.

Precisamos definir como o modelo de dados suportará essa operação. O CSV bruto traz todas as dimensões de forma denormalizada ("flat") e com tipos texto. 

## 2. Alternativas consideradas

### A. Opção Nula: Manter o esquema "Flat" (Uma única tabela com tudo em TEXT)
- **Por que é viável:** É exatamente como o CSV de origem e como a camada "bronze" está estruturada atualmente. 
- **Desvantagem:** É inadequado para um sistema transacional OLTP (violaria a 3FN), redundância brutal de dados (ex: salvar o nome e código do município milhões de vezes repetidas), sem validação de integridade referencial. Além disso, falha no requisito central da E1.

### B. Normalização Parcial (Star Schema direto no OLTP)
- **O que oferece:** Cria dimensões separadas (Tempo, Localidade, Empregador) e a tabela Fato, já otimizada para consulta.
- **Desvantagem:** Bancos transacionais (OLTP) sofrem com carga e inserções se modelados diretamente para OLAP (Star Schema) desde a origem, tornando as transações lentas.

### C. Normalização 3FN (Padrão de Sistemas Transacionais)
- **O que oferece:** Estrutura clássica relacional. Separa as entidades auxiliares (CBO, CNAE, Municípios) em tabelas próprias (Domínios) com chaves primárias. A tabela de `movimentacao` guarda as métricas (salário, idade) usando tipos corretos numéricos e chaves estrangeiras (`FOREIGN KEY`) conectando as entidades.
- **Desvantagem:** Exige escrita de joins para as consultas relatoriais (por isso teremos o Data Lake / Data Warehouse nas entregas seguintes).

## 3. Medição e Prototipação

Foi verificado no PostgreSQL 16 local que a tabela em TEXT da camada Bronze gasta substancialmente mais disco que uma tabela com tipos numéricos corretos (`INT`, `NUMERIC(10,2)`). O tempo para ingestão em lote com `COPY` mantém-se na casa dos segundos, mas os índices (B-Tree nas chaves estrangeiras) adicionam leve _overhead_ de inserção (perfeitamente aceitável para o requisito de simular a origem).

## 4. Decisão

**Escolhemos a Alternativa C (Normalização 3FN)** para simular o banco de origem OLTP do METRA, garantindo restrições estruturais de integridade e tipos primitivos reais antes de levarmos os dados para o Data Lake.

## 5. Consequências e Tradeoffs

### O que se ganha
- Simulamos um ambiente de produção fiel aos sistemas corporativos modernos.
- Integridade do dado: A sujeira do dado bruto esbarra nas `FOREIGN KEYS` e `NOT NULL`.
- Economia de armazenamento no SGBD relacional por tipagem forte.

### O que se perde ou se compromete
- O script de carga precisará de uma etapa para preencher as tabelas auxiliares (município, CBO, etc) antes de popular a tabela principal de movimentações.

### O que se torna irreversível ou restringe o sistema futuro
- Se uma empresa submeter um município inválido, o banco negará o dado inteiro.

## 6. Gatilho de Revisão

Se a ingestão do volume completo da série histórica na origem OLTP ultrapassar **10 minutos**, devido à checagem massiva de chaves estrangeiras, precisaremos rever a aplicação de _constraints_ ou desabilitá-las temporariamente durante o _bulk load_ inicial.
