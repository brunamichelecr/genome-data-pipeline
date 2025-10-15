import os
import psycopg2
import bcrypt

# ⚠️ O código SQL que você forneceu para criar as tabelas
SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS public.analises
(
    id_analise serial NOT NULL,
    id_usuario integer,
    data timestamp without time zone,
    status character varying(50) COLLATE pg_catalog."default",
    descricao text COLLATE pg_catalog."default",
    CONSTRAINT analises_pkey PRIMARY KEY (id_analise)
);

CREATE TABLE IF NOT EXISTS public.diseases
(
    id_disease serial NOT NULL,
    disease_name character varying(100) COLLATE pg_catalog."default",
    disease_desc text COLLATE pg_catalog."default",
    disease_name_pt character varying(100) COLLATE pg_catalog."default",
    disease_synonym text COLLATE pg_catalog."default",
    mesh_id "char",
    disease_desc_pt text COLLATE pg_catalog."default",
    breve_desc text COLLATE pg_catalog."default",
    CONSTRAINT diseases_pkey PRIMARY KEY (id_disease)
);

CREATE TABLE IF NOT EXISTS public.genes
(
    id_gene serial NOT NULL,
    id_disease integer,
    gene_symbol character varying(50) COLLATE pg_catalog."default",
    gene_desc text COLLATE pg_catalog."default",
    CONSTRAINT genes_pkey PRIMARY KEY (id_gene)
);

CREATE TABLE IF NOT EXISTS public.raw_data
(
    id_raw_data serial NOT NULL,
    id_usuario integer,
    id_snp integer,
    data_upload timestamp without time zone,
    CONSTRAINT raw_data_pkey PRIMARY KEY (id_raw_data)
);

CREATE TABLE IF NOT EXISTS public.raw_json
(
    id_raw serial NOT NULL,
    id_ref integer,
    fonte character varying(100) COLLATE pg_catalog."default",
    payload jsonb,
    data_ingestao timestamp without time zone,
    CONSTRAINT raw_json_pkey PRIMARY KEY (id_raw)
);

CREATE TABLE IF NOT EXISTS public.referencias
(
    id_ref serial NOT NULL,
    base_origem character varying(100) COLLATE pg_catalog."default",
    url text COLLATE pg_catalog."default",
    data_coleta timestamp without time zone,
    CONSTRAINT referencias_pkey PRIMARY KEY (id_ref)
);

CREATE TABLE IF NOT EXISTS public.snps
(
    id_snp serial NOT NULL,
    rsid character varying(50) COLLATE pg_catalog."default",
    posicao_genomica character varying(50) COLLATE pg_catalog."default",
    referencia character varying(50) COLLATE pg_catalog."default",
    efeito text COLLATE pg_catalog."default",
    CONSTRAINT snps_pkey PRIMARY KEY (id_snp)
);

CREATE TABLE IF NOT EXISTS public.usuarios
(
    id_usuario serial NOT NULL,
    email character varying(50) COLLATE pg_catalog."default" NOT NULL,
    senha_hash character varying(100) COLLATE pg_catalog."default" NOT NULL,
    genero character(1) COLLATE pg_catalog."default",
    nome character varying(100) COLLATE pg_catalog."default",
    criado_em timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario),
    CONSTRAINT email_unico UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS public.variacao_snps
(
    id_variacao integer NOT NULL,
    id_snp integer NOT NULL,
    CONSTRAINT variacao_snps_pkey PRIMARY KEY (id_variacao, id_snp)
);

CREATE TABLE IF NOT EXISTS public.variacoes
(
    id_variacao serial NOT NULL,
    id_gene integer,
    variacao character varying(50) COLLATE pg_catalog."default",
    alelo character varying(10) COLLATE pg_catalog."default",
    risco text COLLATE pg_catalog."default",
    CONSTRAINT variacoes_pkey PRIMARY KEY (id_variacao)
);

ALTER TABLE IF EXISTS public.analises
    ADD CONSTRAINT analises_id_usuario_fkey FOREIGN KEY (id_usuario)
    REFERENCES public.usuarios (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.genes
    ADD CONSTRAINT genes_id_disease_fkey FOREIGN KEY (id_disease)
    REFERENCES public.diseases (id_disease) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.raw_data
    ADD CONSTRAINT raw_data_id_snp_fkey FOREIGN KEY (id_snp)
    REFERENCES public.snps (id_snp) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.raw_data
    ADD CONSTRAINT raw_data_id_usuario_fkey FOREIGN KEY (id_usuario)
    REFERENCES public.usuarios (id_usuario) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.raw_json
    ADD CONSTRAINT raw_json_id_ref_fkey FOREIGN KEY (id_ref)
    REFERENCES public.referencias (id_ref) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.variacao_snps
    ADD CONSTRAINT variacao_snps_id_snp_fkey FOREIGN KEY (id_snp)
    REFERENCES public.snps (id_snp) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.variacao_snps
    ADD CONSTRAINT variacao_snps_id_variacao_fkey FOREIGN KEY (id_variacao)
    REFERENCES public.variacoes (id_variacao) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.variacoes
    ADD CONSTRAINT variacoes_id_gene_fkey FOREIGN KEY (id_gene)
    REFERENCES public.genes (id_gene) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
"""

def init_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Erro: Variável de ambiente DATABASE_URL não encontrada.")
        return

    conn = None
    try:
        print("Conectando ao banco de dados...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # 1. Executa o SQL para criar as tabelas
        print("Executando script de criação de schema...")
        cur.execute(SQL_SCHEMA)
        conn.commit()
        print("Schema do banco de dados criado com sucesso.")

        # 2. Insere o usuário administrador com hash de senha
        admin_email = "brunamichelecr@gmail.com"
        admin_pass_plaintext = "cacto1012" 
        
        # Gera o hash de forma segura
        senha_bytes = admin_pass_plaintext.encode('utf-8')
        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
        
        # Insere o usuário. ON CONFLICT evita erros se o usuário já existir.
        print(f"Adicionando usuário administrador: {admin_email}")
        cur.execute(
            "INSERT INTO public.usuarios (email, senha_hash, nome) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING;", 
            (admin_email, senha_hash, 'Bruna Admin')
        )
        conn.commit()
        print("Usuário administrador inserido com hash de senha.")
        
    except ImportError:
        print("Não foi possível importar o bcrypt. As tabelas foram criadas, mas o usuário administrador NÃO foi inserido por segurança.")
    except psycopg2.Error as e:
        print(f"Ocorreu um erro ao inicializar o banco de dados: {e}")
        if conn:
            conn.rollback() # Reverte em caso de erro
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()