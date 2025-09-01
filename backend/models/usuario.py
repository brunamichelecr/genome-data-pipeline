import bcrypt
from db import get_connection
import psycopg2

def cadastrar_usuario(nome, genero, email, senha):
    conn = get_connection()
    cur = conn.cursor()

    # Gerar hash seguro da senha
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cur.execute("""
            INSERT INTO usuarios (nome, genero, email, senha_hash)
            VALUES (%s, %s, %s, %s)
        """, (nome, genero, email, senha_hash))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False, "E-mail já cadastrado."

    except Exception as e:
        conn.rollback()
        print("Erro ao cadastrar:", e)
        return False, "Erro ao cadastrar usuário."

    finally:
        cur.close()
        conn.close()