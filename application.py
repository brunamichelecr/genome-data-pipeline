import os
import bcrypt
from flask import (
    Flask, request, jsonify, render_template,
    session, redirect, url_for, flash
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from models.usuario import cadastrar_usuario
from models.disease import Disease
from db import get_connection

application = Flask(__name__) # Nome da aplicação
CORS(application)             # Uso consistente do nome

# ——————————————————————————————
# Configurações gerais
# ——————————————————————————————
# CORRIGIDO: Agora usa 'application'
application.secret_key = os.getenv('SECRET_KEY', 'troque_esta_chave_em_producao')
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ——————————————————————————————
# Configuração de uploads
# ——————————————————————————————
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return (
        filename
        and '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ——————————————————————————————
# Inicialização do ORM
# ——————————————————————————————
orm_db = SQLAlchemy(application)

# ——————————————————————————————
# Rota raiz (landing page)
# ——————————————————————————————
@application.route('/', methods=['GET'])
def home():
    if session.get('user_id'):
        return redirect(url_for('resultados'))
    return render_template('index.html')

# ——————————————————————————————
# Cadastro de usuário
# ——————————————————————————————
@application.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')

    nome = request.form.get('nome')
    genero = request.form.get('genero')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not all([nome, genero, email, senha]):
        flash('Todos os campos são obrigatórios.', 'warning')
        return render_template('cadastro.html')

    sucesso, mensagem = cadastrar_usuario(nome, genero, email, senha)
    flash(mensagem, 'success' if sucesso else 'danger')
    if sucesso:
        return redirect(url_for('login'))
    return render_template('cadastro.html')

# ——————————————————————————————
# Login / Logout
# ——————————————————————————————
@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email')
    senha = request.form.get('senha')

    if not email or not senha:
        flash('Preencha e-mail e senha.', 'warning')
        return render_template('login.html')

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id_usuario, senha_hash FROM usuarios WHERE email = %s",
            (email,)
        )
        row = cur.fetchone()
        if row:
            user_id, stored_hash = row
            if bcrypt.checkpw(senha.encode('utf-8'), stored_hash.encode('utf-8')):
                session['user_id'] = user_id
                return redirect(url_for('carregar_dados'))

        flash('E-mail ou senha inválidos.', 'danger')

    except Exception as e:
        print('Erro no login:', e)
        flash('Erro interno. Tente novamente.', 'danger')
    finally:
        cur.close()
        conn.close()

    return render_template('login.html')

@application.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    # volta à landing page não-logada
    return redirect(url_for('home'))

# ——————————————————————————————
# Upload de dados (CSV)
# ——————————————————————————————
@application.route('/carregar_dados', methods=['GET', 'POST'])
def carregar_dados():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    save_path = os.path.join(application.config['UPLOAD_FOLDER'], f"{user_id}.csv")
    already = os.path.exists(save_path)

    if request.method == 'POST':
        if already:
            flash('Arquivo já enviado.', 'info')
            return redirect(url_for('carregar_dados'))

        file = request.files.get('file')
        if not file or file.filename == '':
            flash('Selecione um arquivo válido.', 'warning')
            return redirect(url_for('carregar_dados'))

        if not allowed_file(file.filename):
            flash('Apenas arquivos .csv são permitidos.', 'warning')
            return redirect(url_for('carregar_dados'))

        filename = secure_filename(f"{user_id}.csv")
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        flash('Upload realizado com sucesso!', 'success')
        return redirect(url_for('carregar_dados'))

    return render_template('carregar_dados.html', already=already)

# ——————————————————————————————
# Páginas estáticas
# ——————————————————————————————
@application.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

@application.route('/contato', methods=['GET'])
def contato():
    return render_template('contato.html')

# ——————————————————————————————
# Resultados (rota protegida)
# ——————————————————————————————
@application.route('/resultados', methods=['GET'])
def resultados():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    doencas = []
    for idx, d in enumerate(orm_db.session.query(Disease).all(), start=1):
        score = getattr(d, 'risk_score', 0.75)
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

# ——————————————————————————————
# APIs de cadastro e verificação de e-mail
# ——————————————————————————————
@application.route('/api/cadastro', methods=['POST'])
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
        print('Erro ao verificar e-mail:', e)
        return jsonify({"erro": "Erro ao verificar e-mail."}), 500
    finally:
        cur.close()
        conn.close()

    sucesso, mensagem = cadastrar_usuario(nome, genero, email, senha)
    status = 201 if sucesso else 400
    return jsonify({"mensagem": mensagem}), status

@application.route('/api/verificar-email', methods=['GET'])
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
        print('Erro ao verificar e-mail:', e)
        return jsonify({"erro": "Erro ao verificar e-mail."}), 500
    finally:
        cur.close()
        conn.close()

# ——————————————————————————————
# Inicialização do app
# ——————————————————————————————
if __name__ == '__main__':
    print("Servidor Flask iniciado em http://localhost:5000")
    application.run(debug=True, port=5000)