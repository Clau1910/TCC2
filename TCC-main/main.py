import os
import mysql.connector
from flask import Flask, request, redirect, url_for, render_template, jsonify, session, flash

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Para sessões e flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Certificar que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/base')
def base():
    return render_template('base.html')

# Configuração do Banco de Dados
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Altere para seu usuário do MySQL
    'password': 'password',  # Altere para sua senha do MySQL
    'database': 'gestao_tempo'
}

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        app.logger.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Verifica se o arquivo tem uma extensão válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '').strip()

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()

            if usuario:
                session['usuario_id'] = usuario['id']
                session['usuario_nome'] = usuario['nome']
                return redirect(url_for('index'))
            else:
                flash('Email ou senha inválidos.')
                return redirect(url_for('login'))
        else:
            flash('Erro ao conectar ao banco de dados.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_materia', methods=['POST', 'GET'])
@login_required
def add_materia():
    if request.method == 'POST':
        nome_materia = request.form.get('nome_materia', '').strip()
        professor = request.form.get('professor', '').strip()
        horario = request.form.get('horario', '').strip()
        foto = request.files.get('foto')
        usuario_id = session.get('usuario_id')

        if not nome_materia:
            flash("Erro: Nome da matéria é obrigatório.")
            return redirect(request.url)

        filename = "default.jpg"
        if foto and allowed_file(foto.filename):
            filename = f"materia_{nome_materia}_{foto.filename}"
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(foto_path)

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO materias (usuario_id, nome, professor, horario, foto) VALUES (%s, %s, %s, %s, %s)",
                           (usuario_id, nome_materia, professor, horario, filename))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('list_materias'))
        else:
            flash("Erro ao conectar ao banco de dados.")
            return redirect(request.url)

    return render_template('add_materia.html')

class MateriaObj:
    def __init__(self, d):
        self.__dict__ = d

@app.route('/list_materias')
@login_required
def list_materias():
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materias WHERE usuario_id = %s", (usuario_id,))
        materias_dicts = cursor.fetchall()
        cursor.close()
        conn.close()
        if materias_dicts:
            print("DEBUG keys in materias_dicts[0]:", list(materias_dicts[0].keys()))
        materias = [MateriaObj(d) for d in materias_dicts]
        return render_template('list_materias.html', materias=materias)
    else:
        flash("Erro ao conectar ao banco de dados.")
        return redirect(url_for('index'))

@app.route('/test_db_connection')
def test_db_connection():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'success', 'message': 'Conexão com o banco de dados bem-sucedida!'})

    else:
        return jsonify({'status': 'error', 'message': 'Falha na conexão com o banco de dados.'}), 500

@app.route('/list_tarefas')
@login_required
def list_tarefas():
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefas WHERE usuario_id = %s", (usuario_id,))
        tarefas = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('list_tarefas.html', tarefas=tarefas)
    else:
        flash("Erro ao conectar ao banco de dados.")
        return redirect(url_for('index'))

@app.route('/add_tarefa', methods=['POST', 'GET'])
def add_tarefa():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        data_entrega = request.form.get('data_entrega', '').strip()
        materia_id = request.form.get('materia_id', '').strip()

        if not titulo or not descricao or not data_entrega or not materia_id:
            return "Erro: Todos os campos são obrigatórios.", 400

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tarefas (titulo, descricao, data_entrega, materia_id) VALUES (%s, %s, %s, %s)",
                           (titulo, descricao, data_entrega, materia_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('list_tarefas'))
        else:
            return "Erro ao conectar ao banco de dados.", 500

    return render_template('add_tarefa.html')

@app.route('/edit_tarefa/<int:id_tarefa>', methods=['POST', 'GET'])
def edit_tarefa(id_tarefa):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefas WHERE id_tarefa = %s", (id_tarefa,))
        tarefa = cursor.fetchone()
        cursor.close()
        conn.close()

        if request.method == 'POST':
            titulo = request.form.get('titulo', '').strip()
            descricao = request.form.get('descricao', '').strip()
            data_entrega = request.form.get('data_entrega', '').strip()

            if not titulo or not descricao or not data_entrega:
                return "Erro: Todos os campos são obrigatórios.", 400

            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tarefas SET titulo = %s, descricao = %s, data_entrega = %s WHERE id_tarefa = %s",
                               (titulo, descricao, data_entrega, id_tarefa))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('list_tarefas'))
            else:
                return "Erro ao conectar ao banco de dados.", 500

        return render_template('edit_tarefa.html', tarefa=tarefa)
    else:
        return "Erro ao conectar ao banco de dados.", 500

@app.route('/delete_tarefa/<int:id_tarefa>', methods=['DELETE'])
def delete_tarefa(id_tarefa):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id_tarefa = %s", (id_tarefa,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Tarefa excluída com sucesso!'})
    else:
        return jsonify({'status': 'error', 'message': 'Erro ao conectar ao banco de dados.'}), 500

@app.route('/edit_materia/<int:id>', methods=['POST', 'GET'])
def edit_materia(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materias WHERE id = %s", (id,))
        materia = cursor.fetchone()
        cursor.close()
        conn.close()

        if request.method == 'POST':
            nome_materia = request.form.get('nome_materia', '').strip()
            professor = request.form.get('professor', '').strip()
            horario = request.form.get('horario', '').strip()

            if not nome_materia or not professor or not horario:
                return "Erro: Todos os campos são obrigatórios.", 400

            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE materias SET nome = %s, professor = %s, horario = %s WHERE id = %s",
                               (nome_materia, professor, horario, id))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('list_materias'))
            else:
                return "Erro ao conectar ao banco de dados.", 500

        return render_template('edit_materia.html', materia=materia)
    else:
        return "Erro ao conectar ao banco de dados.", 500

@app.route('/delete_materia/<int:id>', methods=['POST', 'GET'])
def delete_materia(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('list_materias'))
    else:
        flash("Erro ao conectar ao banco de dados.")
        return redirect(url_for('list_materias'))

app.run(host='0.0.0.0', port= 5001, debug=True)
