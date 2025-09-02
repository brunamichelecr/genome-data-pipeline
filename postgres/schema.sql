-- Tabela de usuários
CREATE TABLE usuarios (
  id_usuario SERIAL PRIMARY KEY,         -- Identificador único do usuário
  nome TEXT NOT NULL,                    -- Nome completo
  genero TEXT NOT NULL,                  -- Sexo do usuário (M/F/O/N)
  email TEXT UNIQUE NOT NULL,            -- Email/login do usuário
  senha_hash TEXT NOT NULL,              -- Senha criptografada
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Data de criação do registro
);

-- Tabela de doenças genéticas
CREATE TABLE diseases (
  id_disease SERIAL PRIMARY KEY,        -- Identificador único da doença
  disease_name VARCHAR(100),            -- Nome da doença
  disease_desc TEXT,                      -- Descrição detalhada
  disease_name_pt VARCHAR(100),  -- Nome da doença em português
  disease_synonym TEXT,                  -- Sinônimos em inglês (uso interno)
  mesh_id VARCHAR(15),                    -- Identificador da doença no MeSH
  disease_desc_pt TEXT,                   --Descrição detalhada em português
  breve_desc TEXT;                        -- Breve descrição em português
);

-- Tabela de genes associados às doenças
CREATE TABLE genes (
  id_gene SERIAL PRIMARY KEY,           -- Identificador único do gene
  id_disease INT REFERENCES diseases(id_disease), -- FK para a doença
  gene_symbol VARCHAR(50),              -- Símbolo do gene (ex: BRCA1)
  gene_desc TEXT                        -- Descrição do gene
);

-- Tabela de variações genéticas
CREATE TABLE variacoes (
  id_variacao SERIAL PRIMARY KEY,       -- Identificador único da variação
  id_gene INT REFERENCES genes(id_gene), -- FK para o gene
  variacao VARCHAR(50),                 -- Tipo de variação (ex: deleção, inserção)
  alelo VARCHAR(10),                    -- Alelo observado
  risco TEXT                            -- Risco associado à variação (ex: alto, moderado)
);

-- Tabela de SNPs (Single Nucleotide Polymorphisms)
CREATE TABLE snps (
  id_snp SERIAL PRIMARY KEY,            -- Identificador único do SNP
  rsid VARCHAR(50),                     -- ID do SNP (ex: rs123456)
  posicao_genomica VARCHAR(50),         -- Posição no genoma
  referencia VARCHAR(50),               -- Alelo de referência
  efeito TEXT                           -- Efeito funcional do SNP
);

-- Tabela de associação muitos-para-muitos entre variações e SNPs
CREATE TABLE variacao_snps (
  id_variacao INT REFERENCES variacoes(id_variacao), -- FK para variação
  id_snp INT REFERENCES snps(id_snp),                -- FK para SNP
  PRIMARY KEY (id_variacao, id_snp)                 -- Chave composta
);

-- Tabela de dados brutos enviados pelos usuários
CREATE TABLE raw_data (
  id_raw_data SERIAL PRIMARY KEY,       -- Identificador único do upload
  id_usuario INT REFERENCES usuarios(id_usuario), -- FK para usuário
  id_snp INT REFERENCES snps(id_snp),   -- FK para SNP referenciado
  data_upload TIMESTAMP                  -- Data e hora do upload
);

-- Tabela de análises realizadas pelos usuários
CREATE TABLE analises (
  id_analise SERIAL PRIMARY KEY,        -- Identificador único da análise
  id_usuario INT REFERENCES usuarios(id_usuario), -- FK para usuário
  data TIMESTAMP,                        -- Data da análise
  status VARCHAR(50),                    -- Status da análise (ex: pendente, concluída)
  descricao TEXT                         -- Descrição da análise
);

-- Tabela de referências externas utilizadas
CREATE TABLE referencias (
  id_ref SERIAL PRIMARY KEY,             -- Identificador único da referência
  base_origem VARCHAR(100),              -- Nome da base de origem (ex: ClinVar)
  url TEXT,                              -- URL da referência
  data_coleta TIMESTAMP                   -- Data de coleta
);

-- Tabela de ingestão de dados em formato JSON
CREATE TABLE raw_json (
  id_raw SERIAL PRIMARY KEY,             -- Identificador único do JSON
  id_ref INT REFERENCES referencias(id_ref), -- FK para referência
  fonte VARCHAR(100),                     -- Fonte do dado (ex: API externa)
  payload JSONB,                          -- Conteúdo JSON armazenado
  data_ingestao TIMESTAMP                 -- Data de ingestão
);
