import os
import mysql.connector
from flask import Flask, request, redirect, url_for, render_template, jsonify, session, flash

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Para sessões e flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import json

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    # Aqui você pode buscar o usuário no banco de dados e retornar um objeto User completo
    # Para simplificação, retornamos um User com o id
    return User(user_id)

@app.before_request
def before_request():
    from flask import g
    g.user = current_user

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

from flask_login import login_required

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
                user = User(usuario['id'])
                login_user(user)
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
    logout_user()
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

class TarefaObj:
    def __init__(self, d):
        self.__dict__ = d
        # Map DB fields to template expected attributes
        self.titulo = d.get('nome')
        self.data_entrega = d.get('prazo')
        self.id_tarefa = d.get('id')

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
    import datetime
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefas WHERE usuario_id = %s", (usuario_id,))
        tarefas_dicts = cursor.fetchall()
        cursor.close()
        conn.close()
        tarefas = []
        for d in tarefas_dicts:
            tarefa = TarefaObj(d)
            # Convert data_entrega to datetime object for template formatting
            if tarefa.data_entrega and isinstance(tarefa.data_entrega, str):
                try:
                    tarefa.data_entrega = datetime.datetime.strptime(tarefa.data_entrega, '%Y-%m-%d')
                except ValueError:
                    tarefa.data_entrega = None
            if tarefa.id_tarefa is not None:
                tarefas.append(tarefa)
        return render_template('list_tarefas.html', tarefas=tarefas)
    else:
        flash("Erro ao conectar ao banco de dados.")
        return redirect(url_for('index'))

import datetime

@app.route('/add_tarefa', methods=['POST', 'GET'])
@login_required
def add_tarefa():
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        prazo_str = request.form.get('data_entrega', '').strip()
        materia_id = request.form.get('materia_id', '').strip()

        print(f"DEBUG: Dados recebidos - titulo: {nome}, descricao: {descricao}, data_entrega: {prazo_str}, materia_id: {materia_id}, usuario_id: {usuario_id}")

        if not nome or not descricao or not prazo_str or not materia_id:
            print("DEBUG: Falha na validação dos campos obrigatórios")
            return "Erro: Todos os campos são obrigatórios.", 400

        try:
            prazo = datetime.datetime.strptime(prazo_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            flash("Erro: Formato de data inválido. Use o seletor de data para escolher a data corretamente.")
            print("DEBUG: Formato de data inválido")
            return redirect(url_for('add_tarefa'))

        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO tarefas (nome, descricao, prazo, materia_id, usuario_id) VALUES (%s, %s, %s, %s, %s)",
                               (nome, descricao, prazo, materia_id, usuario_id))
                conn.commit()
                print("DEBUG: Inserção realizada com sucesso")
            except Exception as e:
                print(f"DEBUG: Erro na inserção: {e}")
                conn.rollback()
                return f"Erro ao inserir tarefa: {e}", 500
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for('list_tarefas'))
        else:
            print("DEBUG: Falha na conexão com o banco de dados")
            return "Erro ao conectar ao banco de dados.", 500

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materias WHERE usuario_id = %s", (usuario_id,))
        materias = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('add_tarefa.html', materias=materias)
    else:
        print("DEBUG: Falha na conexão com o banco de dados para carregar matérias")
        return "Erro ao conectar ao banco de dados.", 500

from flask_login import login_required

@app.route('/edit_tarefa/<int:id_tarefa>', methods=['POST', 'GET'])
@login_required
def edit_tarefa(id_tarefa):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id_tarefa,))
        tarefa = cursor.fetchone()
        cursor.close()
        conn.close()

        if request.method == 'POST':
            titulo = request.form.get('titulo', '').strip()
            descricao = request.form.get('descricao', '').strip()
            data_entrega = request.form.get('data_entrega', '').strip()
            foto = request.files.get('foto')

            if not titulo or not descricao or not data_entrega:
                return "Erro: Todos os campos são obrigatórios.", 400

            # Convertendo data_entrega para o formato YYYY-MM-DD
            import datetime
            try:
                data_entrega_obj = datetime.datetime.strptime(data_entrega, '%Y-%m-%d')
            except ValueError:
                try:
                    data_entrega_obj = datetime.datetime.strptime(data_entrega, '%d/%m/%Y')
                except ValueError:
                    return "Erro: Formato de data inválido.", 400
            data_entrega_formatada = data_entrega_obj.strftime('%Y-%m-%d')

            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tarefas SET nome = %s, descricao = %s, prazo = %s WHERE id = %s",
                               (titulo, descricao, data_entrega_formatada, id_tarefa))
                conn.commit()

                # Processar upload da foto se houver
                if foto and foto.filename != '' and allowed_file(foto.filename):
                    filename = secure_filename(f"tarefa_{id_tarefa}_{foto.filename}")
                    foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    foto.save(foto_path)
                    # Inserir registro na tabela atividades_fotos
                    cursor.execute("INSERT INTO atividades_fotos (usuario_id, tarefa_id, foto) VALUES (%s, %s, %s)",
                                   (session.get('usuario_id'), id_tarefa, filename))
                    conn.commit()

                cursor.close()
                conn.close()
                return redirect(url_for('list_tarefas'))
            else:
                return "Erro ao conectar ao banco de dados.", 500

        return render_template('edit_tarefa.html', tarefa=tarefa)
    else:
        return "Erro ao conectar ao banco de dados.", 500

@app.route('/delete_tarefa/<int:id_tarefa>', methods=['POST'])
@login_required
def delete_tarefa(id_tarefa):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = %s", (id_tarefa,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('list_tarefas'))
    else:
        flash("Erro ao conectar ao banco de dados.")
        return redirect(url_for('list_tarefas'))

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

import os

@app.route('/delete_materia/<int:id>', methods=['POST', 'GET'])
def delete_materia(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        # Buscar o nome do arquivo da foto antes de deletar
        cursor.execute("SELECT foto FROM materias WHERE id = %s", (id,))
        materia = cursor.fetchone()
        foto_filename = materia['foto'] if materia else None

        # Deletar a matéria do banco
        cursor.execute("DELETE FROM materias WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Apagar o arquivo da foto se existir e não for o padrão
        if foto_filename and foto_filename != "default.jpg":
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_filename)
            if os.path.exists(foto_path):
                os.remove(foto_path)

        return redirect(url_for('list_materias'))
    else:
        flash("Erro ao conectar ao banco de dados.")
        return redirect(url_for('list_materias'))

@app.route('/debug_tarefas')
@login_required
def debug_tarefas():
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM tarefas")
        columns = cursor.fetchall()
        cursor.execute("SELECT * FROM tarefas LIMIT 5")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            'columns': columns,
            'rows': rows,
            'usuario_id': usuario_id
        })
    else:
        return jsonify({'error': 'Erro ao conectar ao banco de dados.'}), 500

# Rota para upload de fotos das tarefas
@app.route('/upload_foto_tarefa/<int:tarefa_id>', methods=['POST'])
@login_required
def upload_foto_tarefa(tarefa_id):
    if 'foto' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    foto = request.files['foto']
    if foto.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    if foto and allowed_file(foto.filename):
        filename = secure_filename(f"tarefa_{tarefa_id}_{foto.filename}")
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(foto_path)

        usuario_id = session.get('usuario_id')
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO atividades_fotos (usuario_id, tarefa_id, foto) VALUES (%s, %s, %s)",
                           (usuario_id, tarefa_id, filename))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'message': 'Foto enviada com sucesso', 'filename': filename}), 200
        else:
            return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500
    else:
        return jsonify({'error': 'Arquivo não permitido'}), 400

# Rota para listar fotos de uma tarefa
@app.route('/fotos_tarefa/<int:tarefa_id>', methods=['GET'])
@login_required
def fotos_tarefa(tarefa_id):
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT foto FROM atividades_fotos WHERE tarefa_id = %s AND usuario_id = %s", (tarefa_id, usuario_id))
        fotos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(fotos)
    else:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

# Rota para fornecer eventos das tarefas para o FullCalendar
@app.route('/tarefas_events', methods=['GET'])
@login_required
def tarefas_events():
    usuario_id = session.get('usuario_id')
    materia_id = request.args.get('materia_id', None)
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if materia_id and materia_id != 'all':
            cursor.execute("SELECT id, nome, descricao, prazo FROM tarefas WHERE usuario_id = %s AND materia_id = %s", (usuario_id, materia_id))
        else:
            cursor.execute("SELECT id, nome, descricao, prazo FROM tarefas WHERE usuario_id = %s", (usuario_id,))
        tarefas = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tarefas)
    else:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

# Rota para listar matérias para o filtro
@app.route('/materias_list', methods=['GET'])
@login_required
def materias_list():
    usuario_id = session.get('usuario_id')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome FROM materias WHERE usuario_id = %s", (usuario_id,))
        materias = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(materias)
    else:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

app.run(host='0.0.0.0', port= 5001, debug=True)
