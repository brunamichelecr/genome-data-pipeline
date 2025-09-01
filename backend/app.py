from flask import Flask, request, jsonify
from flask_cors import CORS
from models.usuario import cadastrar_usuario

app = Flask(__name__)
CORS(app)

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    nome = data.get('nome')
    genero = data.get('genero')
    email = data.get('email')
    senha = data.get('senha')

    if not all([nome, genero, email, senha]):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    sucesso, mensagem = cadastrar_usuario(nome, genero, email, senha)
    status = 201 if sucesso else 400
    return jsonify({"mensagem": mensagem}), status

if __name__ == '__main__':
    app.run(debug=True, port=5000)