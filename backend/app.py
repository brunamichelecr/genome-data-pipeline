from flask import Flask, request, jsonify
from flask_cors import CORS
from models.usuario import cadastrar_usuario
from db import get_connection

app = Flask(__name__)
# Habilita CORS para permitir chamadas de outros domínios (importante em apps frontend separados)
CORS(app)

# -------------------------------
# Rota principal de cadastro
# -------------------------------
@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    # Recebe o payload enviado em JSON pelo cliente
    data = request.get_json()

    # Extrai os campos obrigatórios
    nome = data.get('nome')
    genero = data.get('genero')
    email = data.get('email')
    senha = data.get('senha')

    # Validação inicial para evitar dados incompletos
    if not all([nome, genero, email, senha]):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    # Verificação prévia de e-mail duplicado antes de chamar a função de cadastro
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT 1 FROM usuarios WHERE email = %s", (email,))
        if cur.fetchone():
            # Se já existe, retorna HTTP 409 (Conflict) → prática REST correta
            return jsonify({"erro": "E-mail já cadastrado."}), 409
    except Exception as e:
        # Erros de consulta ao banco (ex: indisponibilidade)
        print("Erro ao verificar e-mail:", e)
        return jsonify({"erro": "Erro ao verificar e-mail."}), 500
    finally:
        cur.close()
        conn.close()

    # Chama a função de cadastro (já responsável por gerar hash da senha e persistir no banco)
    sucesso, mensagem = cadastrar_usuario(nome, genero, email, senha)

    # Se deu certo, retorna HTTP 201 (Created), senão 400 (Bad Request)
    status = 201 if sucesso else 400
    return jsonify({"mensagem": mensagem}), status


# -------------------------------
# Rota de verificação de e-mail duplicado (usada pelo frontend em tempo real)
# -------------------------------
@app.route('/api/verificar-email', methods=['GET'])
def verificar_email():
    # Captura e-mail vindo como query param (ex: /api/verificar-email?email=teste@teste.com)
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


# -------------------------------
# Inicialização da aplicação
# -------------------------------
if __name__ == '__main__':
    # debug=True → reinicia automaticamente e mostra traceback (bom em dev, ruim em produção)
    app.run(debug=True, port=5000)
