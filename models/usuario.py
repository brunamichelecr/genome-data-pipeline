import bcrypt
from db import get_connection
import psycopg2

def cadastrar_usuario(nome, genero, email, senha):
    # Obtém conexão com o banco de dados (PostgreSQL, no caso)
    conn = get_connection()
    cur = conn.cursor()

    # Gera um hash seguro para a senha antes de salvar no banco
    # bcrypt utiliza salt internamente, garantindo mais segurança contra ataques de dicionário e força bruta
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        # Insere um novo usuário na tabela, garantindo que a senha nunca seja armazenada em texto puro
        cur.execute("""
            INSERT INTO usuarios (nome, genero, email, senha_hash)
            VALUES (%s, %s, %s, %s)
        """, (nome, genero, email, senha_hash))

        # Confirma a transação no banco
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"

    except psycopg2.errors.UniqueViolation:
        # Caso o e-mail já exista (restrição UNIQUE), desfaz a transação
        conn.rollback()
        return False, "E-mail já cadastrado."

    except Exception as e:
        # Captura outras exceções (problema de conexão, sintaxe SQL, etc.)
        conn.rollback()
        print("Erro ao cadastrar:", e)
        return False, "Erro ao cadastrar usuário."

    finally:
        # Fecha cursor e conexão, evitando vazamento de recursos
        cur.close()
        conn.close()
