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

# Rota de resultados
@app.route('/resultados', methods=['GET'], endpoint='resultados')
def resultados():
    doencas = orm_db.session.query(Disease).all()

    cards_html = ""
    for d in doencas:
        modal_id = f"modal-{d.id_disease}"
        cards_html += f"""
        <div class="col-md-6 mb-4">
            <div class="card shadow-sm h-100">
                <div class="card-body">
                    <h4 class="card-title text-primary fw-bold">{d.disease_name_pt}</h4>
                    <p class="card-text">{d.breve_desc or '—'}</p>
                    <button class="btn btn-outline-info btn-sm mb-3" data-bs-toggle="modal" data-bs-target="#{modal_id}">
                        Leia mais
                    </button>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar bg-warning" role="progressbar" style="width: 0%;" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                            Risco: 0%
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="{modal_id}" tabindex="-1" aria-labelledby="{modal_id}-label" aria-hidden="true">
            <div class="modal-dialog modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="{modal_id}-label">{d.disease_name_pt}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
                    </div>
                    <div class="modal-body">
                        <p>{d.disease_desc_pt or 'Descrição não disponível.'}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>
        """

    return render_template('resultados.html', cards_html=cards_html)

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

# Inicialização
if __name__ == '__main__':
    print("Servidor Flask iniciado em http://localhost:5000")
    app.run(debug=True, port=5000)