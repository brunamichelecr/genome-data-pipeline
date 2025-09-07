import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models.usuario import cadastrar_usuario
from models.disease import Disease
from db import get_connection

app = Flask(__name__)
CORS(app)

# Configuração do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
orm_db = SQLAlchemy(app)

# Rota da página inicial
@app.route('/', endpoint='home')
def index():
    return render_template('index.html')

# Rota da página de cadastro (visual)
@app.route('/cadastro', endpoint='cadastro')
def cadastro_page():
    return render_template('cadastro.html')

# Rota da página "Sobre nós"
@app.route('/sobre', endpoint='sobre')
def sobre_page():
    return render_template('sobre.html')

# Rota da página "Contato"
@app.route('/contato', endpoint='contato')
def contato_page():
    return render_template('contato.html')

# Rota da página de resultados
@app.route('/resultados', methods=['GET'], endpoint='resultados')
def resultados():
    doencas_db = orm_db.session.query(Disease).all()
    doencas = []

    for idx, d in enumerate(doencas_db, start=1):
        score = getattr(d, 'risk_score', 0.33)
        percent = int(score * 100)
        if score < 0.4:
            bg_class = 'bg-success'
        elif score < 0.7:
            bg_class = 'bg-warning'
        else:
            bg_class = 'bg-danger'

        doencas.append({
            'id': d.id_disease,
            'name': d.disease_name_pt,
            'brief': d.breve_desc or '—',
            'desc': d.disease_desc_pt or 'Descrição não disponível.',
            'percent': percent,
            'bg_class': bg_class,
            'delay': round(0.2 * idx, 1)
        })

    return render_template(
        'resultados.html',
        doencas=doencas,
        page_class='resultados-page'
    )

# Rota de cadastro via API
@app.route('/api/cadastro', methods=['POST'])
def cadastro_api():
    data = request.get_json()
    nome = data.get('nome')
    genero = data.get('genero')
    email = data.get('email')
    senha = data.get('senha')

    if not all([nome, genero, email, senha]):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

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

    sucesso, mensagem = cadastrar_usuario(nome, genero, email, senha)
    status = 201 if sucesso else 400
    return jsonify({"mensagem": mensagem}), status

# Rota de verificação de e-mail via API
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
    print("Servidor Flask iniciado em http://localhost:5000")
    app.run(debug=True, port=5000)