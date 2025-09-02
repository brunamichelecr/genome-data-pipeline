## Data Engineering Pipeline para Análise Genética

## Sobre o Projeto

Este projeto demonstra a construção de um **pipeline completo de engenharia de dados** aplicado à área da **genômica e saúde personalizada**.

A ideia é permitir que um usuário faça upload de um arquivo com seus **SNPs (rsIDs)** e, a partir daí:

1. Consultar APIs públicas do **NCBI (e-utilities)** para identificar **genes associados a doenças**.
2. Buscar **variações genéticas** relacionadas no **ClinVar**.
3. Obter detalhes de **SNPs no dbSNP**, incluindo riscos associados.
4. Estruturar todas as informações em um **banco de dados relacional (PostgreSQL)**.
5. Permitir ao usuário visualizar seus resultados via um **frontend simples (Bootstrap)**.

 O objetivo principal é **demonstrar competências sólidas em engenharia de dados**:

* Integração de múltiplas fontes externas.
* Criação de **pipeline ETL** com staging e transformação.
* Modelagem de **banco de dados relacional**.
* Rastreabilidade e boas práticas de logging.
* Documentação clara e orientada para **uso real em portfólio profissional**.

---

## Arquitetura (Visão Geral)

```mermaid
flowchart LR
    subgraph User["👤 Usuário"]
        A1[Upload CSV com rsIDs]
    end

    subgraph Backend["⚙️ Backend (Python/Flask)"]
        A2[Leitura do CSV]
        A3[Chamada às APIs NCBI e-utilities]
        A4[ETL: staging -> transformação -> carga]
    end

    subgraph DB["🗄️ Banco de Dados (PostgreSQL)"]
        B1[(raw_json - staging)]
        B2[(snps)]
        B3[(variacoes)]
        B4[(genes)]
        B5[(diseases)]
        B6[(usuarios/analises)]
    end

    subgraph Frontend["💻 Frontend (Bootstrap)"]
        C1[Dashboard de Resultados]
    end

    A1 --> A2 --> A3 --> A4
    A4 --> B1 & B2 & B3 & B4 & B5 & B6
    B2 --> C1
    B3 --> C1
    B5 --> C1
```

## Diagrama de Relacionamento DB

```mermaid
erDiagram
    USUARIOS ||--o{ RAW_DATA : envia
    USUARIOS ||--o{ ANALISES : realiza

    DISEASES ||--o{ GENES : possui
    GENES ||--o{ VARIACOES : contém
    VARIACOES ||--o{ VARIACAO_SNPS : está_relacionada
    SNPS ||--o{ VARIACAO_SNPS : está_relacionado
    SNPS ||--o{ RAW_DATA : aparece_em

    REFERENCIAS ||--o{ RAW_JSON : origem

    USUARIOS {
        int id_usuario
        string login
        string senha
        char sexo
        string nome_user
    }

    DISEASES {
        int id_disease
        string disease_name
        text disease_desc
    }

    GENES {
        int id_gene
        int id_disease
        string gene_symbol
        text gene_desc
    }

    VARIACOES {
        int id_variacao
        int id_gene
        string variacao
        string alelo
        text risco
    }

    SNPS {
        int id_snp
        string rsid
        string posicao_genomica
        string referencia
        text efeito
    }

    VARIACAO_SNPS {
        int id_variacao
        int id_snp
    }

    RAW_DATA {
        int id_raw_data
        int id_usuario
        int id_snp
        timestamp data_upload
    }

    ANALISES {
        int id_analise
        int id_usuario
        timestamp data
        string status
        text descricao
    }

    REFERENCIAS {
        int id_ref
        string base_origem
        text url
        timestamp data_coleta
    }

    RAW_JSON {
        int id_raw
        int id_ref
        string fonte
        jsonb payload
        timestamp data_ingestao
    }

```
---

## Como Funciona na Prática

1. O usuário faz upload do seu **CSV** com identificadores de SNP (rsIDs).
2. O backend consome a API do **NCBI e-utilities** para buscar doenças, genes e variações associadas.
3. Os dados crus são armazenados em **staging (raw\_json)** para rastreabilidade.
4. Os dados transformados são organizados em tabelas normalizadas (`snps`, `variacoes`, `genes`, `diseases`).
5. O frontend exibe um **resumo personalizado**, como:

   * Doenças relacionadas ao usuário.
   * Genes impactados.
   * SNPs de maior risco.

---

## Melhorias Futuras (Nível Pleno → Avançado)

* Adicionar **Airflow/Prefect** para orquestração do pipeline.
* Exportar dados em **Parquet/JSON** simulando Data Lake.
* Implementar **testes unitários** para parsing das APIs.
* Containerização com **Docker** (Postgres + Backend).
* Criar caching de consultas às APIs do NCBI.
* Dashboard avançado (Gráficos + estatísticas por gene/doença).

---

Este repositório será atualizado à medida que cada tarefa for concluída.
Objetivo final: um projeto completo de **engenharia de dados aplicada à saúde**.


---


## Obstáculos Técnicos e Desafios Enfrentados

Durante o desenvolvimento do projeto **Genome Data Pipeline**, diversos desafios técnicos surgiram, exigindo adaptações criativas e decisões estratégicas. Abaixo estão os principais obstáculos enfrentados:

- **Limitações de APIs externas**  
  As APIs do NCBI (e-utilities) possuem restrições de taxa e estrutura de resposta complexa. Foi necessário implementar controle de tempo entre requisições e tratamento robusto de erros para garantir a estabilidade do pipeline.

- **Tradução de dados biomédicos**  
  A tradução automática das descrições de doenças (em inglês) para o português apresentou dificuldades. Bibliotecas como `googletrans` deixaram de funcionar em versões recentes do Python (como 3.13), e APIs como DeepL e Google Cloud Translate exigem planos pagos. A solução adotada foi realizar a tradução manual dos textos mais relevantes.

- **Limitações de bibliotecas em Python 3.13**  
  Algumas bibliotecas amplamente utilizadas, como `googletrans`, ainda não são compatíveis com Python 3.13 devido à remoção de módulos como `cgi`. Isso exigiu reavaliação de dependências e busca por alternativas compatíveis.

- **Documentação e visualização**  
  Traduzir a complexidade técnica do pipeline para uma documentação clara e acessível foi um desafio à parte. O objetivo foi tornar o projeto compreensível tanto para profissionais técnicos quanto para recrutadores e colegas de área.
