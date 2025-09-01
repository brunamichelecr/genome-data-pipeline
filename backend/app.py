from flask import Flask, request, jsonify
from flask_cors import CORS
from models.usuario import cadastrar_usuario
from db import get_connection

app = Flask(__name__)
CORS(app)

# Rota principal de cadastro
@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()

    nome = data.get('nome')
    genero = data.get('genero')
    email = data.get('email')
    senha = data.get('senha')

    if not all([nome, genero, email, senha]):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    # Verificação de e-mail duplicado antes de cadastrar
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM usuarios WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"erro": "E-mail já cadastrado."}), 409
    except Exception as e:
        print("Erro ao verificar e-mail:", e)
        return jsonify({"erro": "Erro ao verificar e-mail."}), 500
    finally:
        cur.close()
        conn.close()

    # Cadastro do usuário
    sucesso, mensagem = cadastrar_usuario(nome, genero, email, senha)
    status = 201 if sucesso else 400
    return jsonify({"mensagem": mensagem}), status

# Rota de verificação de e-mail duplicado (usada pelo frontend)
@app.route('/api/verificar-email', methods=['GET'])
def verificar_email():
    email = request.args.get('email')

    if not email:
        return jsonify({"erro": "E-mail não fornecido."}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT 1 FROM usuarios WHERE email = %s", (email,))
        existe = cur.fetchone() is not None
        return jsonify({"existe": existe}), 200
    except Exception as e:
        print("Erro ao verificar e-mail:", e)
        return jsonify({"erro": "Erro ao verificar e-mail."}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)