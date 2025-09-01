import bcrypt
from db import get_connection

def cadastrar_usuario(nome, genero, email, senha):
    conn = get_connection()
    cur = conn.cursor()

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cur.execute("""
            INSERT INTO usuarios (nome, genero, email, senha_hash)
            VALUES (%s, %s, %s, %s)
        """, (nome, genero, email, senha_hash))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except Exception as e:
        if "duplicate key" in str(e):
            return False, "E-mail já cadastrado."
        return False, "Erro ao cadastrar usuário."
    finally:
        cur.close()
        conn.close()