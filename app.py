import os
import bcrypt
from flask import (
    Flask, request, jsonify,
    render_template, session,
    redirect, url_for, flash
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from models.usuario import cadastrar_usuario
from models.disease import Disease
from db import get_connection

app = Flask(__name__)
CORS(app)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'troque_esta_chave_em_producao')

orm_db = SQLAlchemy(app)

# ------------------------
# Páginas estáticas
# ------------------------
@app.route('/', endpoint='home')
def index():
    return render_template('index.html')

@app.route('/cadastro', endpoint='cadastro')
def cadastro_page():
    return render_template('cadastro.html')

@app.route('/sobre', endpoint='sobre')
def sobre_page():
    return render_template('sobre.html')

@app.route('/contato', endpoint='contato')
def contato_page():
    return render_template('contato.html')

# ------------------------
# Autenticação (login/logout)
# ------------------------
@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    senha = request.form.get('senha')
    if not email or not senha:
        flash("Preencha e-mail e senha.", "warning")
        return render_template('login.html')

    conn = get_connection()
    cur = conn.cursor()
    try:
        # Busca PK e hash gerado pelo bcrypt
        cur.execute(
            "SELECT id_usuario, senha_hash FROM usuarios WHERE email = %s",
            (email,)
        )
        row = cur.fetchone()
        if not row:
            flash("E-mail ou senha inválidos.", "danger")
            return render_template('login.html')

        user_id, stored_hash = row
        # Verificação com bcrypt
        if bcrypt.checkpw(senha.encode('utf-8'), stored_hash.encode('utf-8')):
            session['user_id'] = user_id
            return redirect(url_for('resultados'))
        else:
            flash("E-mail ou senha inválidos.", "danger")

    except Exception as e:
        print("Erro no login:", e)
        flash("Erro interno. Tente novamente.", "danger")
    finally:
        cur.close()
        conn.close()

    return render_template('login.html')

@app.route('/logout', endpoint='logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# ------------------------
# Cadastro via API
# ------------------------
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

# ------------------------
# Resultados (rota protegida)
# ------------------------
@app.route('/resultados', methods=['GET'], endpoint='resultados')
def resultados():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    doencas_db = orm_db.session.query(Disease).all()
    doencas = []
    for idx, d in enumerate(doencas_db, start=1):
        score = getattr(d, 'risk_score', 0.75)
        percent = int(score * 100)
        bg_class = 'bg-success' if score < 0.4 else 'bg-warning' if score < 0.7 else 'bg-danger'
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

# ------------------------
# Inicialização
# ------------------------
if __name__ == '__main__':
    print("Servidor Flask iniciado em http://localhost:5000")
    app.run(debug=True, port=5000)