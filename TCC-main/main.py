import os
import mysql.connector
from flask import Flask, request, redirect, url_for, render_template, jsonify

# Configuração do Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Certificar que a pasta de uploads existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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

@app.route('/add_materia', methods=['POST', 'GET'])
def add_materia():
    if request.method == 'POST':
        nome_materia = request.form.get('nome_materia', '').strip()
        professor = request.form.get('professor', '').strip()
        horario = request.form.get('horario', '').strip()
        foto = request.files.get('foto')
        usuario_id = 1  # Simulando um usuário fixo (isso será substituído quando houver login)

        if not nome_materia:
            return "Erro: Nome da matéria é obrigatório.", 400

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
            cursor.close()  # Fecha o cursor
            conn.close()  # Fecha a conexão
            return redirect(url_for('list_materias'))
        else:
            return "Erro ao conectar ao banco de dados.", 500

    return render_template('add_materia.html')

@app.route('/list_materias')
def list_materias():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materias")
        materias = cursor.fetchall()
        cursor.close()  # Fecha o cursor
        conn.close()  # Fecha a conexão
        return render_template('list_materias.html', materias=materias)
    else:
        return "Erro ao conectar ao banco de dados.", 500

@app.route('/test_db_connection')
def test_db_connection():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'success', 'message': 'Conexão com o banco de dados bem-sucedida!'})
    else:
        return jsonify({'status': 'error', 'message': 'Falha na conexão com o banco de dados.'}), 500

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

@app.route('/edit_materia/<int:id_materia>', methods=['POST', 'GET'])
def edit_materia(id_materia):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM materias WHERE id_materia = %s", (id_materia,))
        materia = cursor.fetchone()
        cursor.close()
        conn.close()

        if request.method == 'POST':
            nome_materia = request.form.get('nome_materia', '').strip()
            descricao = request.form.get('descricao', '').strip()
            carga_horaria = request.form.get('carga_horaria', '').strip()
            professor = request.form.get('professor', '').strip()

            if not nome_materia or not descricao or not carga_horaria or not professor:
                return "Erro: Todos os campos são obrigatórios.", 400

            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE materias SET nome = %s, descricao = %s, carga_horaria = %s, professor = %s WHERE id_materia = %s",
                               (nome_materia, descricao, carga_horaria, professor, id_materia))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('list_materias'))
            else:
                return "Erro ao conectar ao banco de dados.", 500

        return render_template('edit_materia.html', materia=materia)
    else:
        return "Erro ao conectar ao banco de dados.", 500

@app.route('/delete_materia/<int:id_materia>', methods=['DELETE'])
def delete_materia(id_materia):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id_materia = %s", (id_materia,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Matéria excluída com sucesso!'})
    else:
        return jsonify({'status': 'error', 'message': 'Erro ao conectar ao banco de dados.'}), 500

app.run(host='0.0.0.0', port= 5001, debug=True)
