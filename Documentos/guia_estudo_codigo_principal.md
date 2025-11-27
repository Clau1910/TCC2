# Guia para Estudo do Código Principal do Projeto Gestão de Tempo

Este guia apresenta explicações detalhadas dos trechos de código mais importantes do arquivo `main.py` da aplicação, com foco nos comandos, bibliotecas, estruturas e fluxos essenciais para compreensão e apresentação do projeto.

---

## 1. Importação de Bibliotecas e Configurações Iniciais

```python
import os
import mysql.connector
from flask import Flask, request, redirect, url_for, render_template, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import datetime
```

- **Flask**: Principal framework web usado para criar rotas, manipular requisições HTTP, sessões, renderizar templates e respostas JSON.
- **mysql.connector**: Biblioteca para conectar e executar queries no banco MySQL.
- **flask_login**: Extensão para gerenciar autenticação e sessões de usuários.
- **werkzeug.utils.secure_filename**: Função para proteger uploads de arquivos contra nomes inseguros.
- **datetime**: Manipulação e validação de datas, especialmente para prazos de tarefas.

---

## 2. Configuração da Aplicação Flask

```python
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave para sessões seguras
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Pasta para uploads de arquivos
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Extensões permitidas
```

- A chave secreta é usada para proteger informações de sessão do usuário.
- Configurações controlam onde os arquivos enviados são armazenados e quais extensões são permitidas.

---

## 3. Configuração do Gerenciador de Login

```python
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
```

- Permite gerenciar sessões e controle de acesso, direcionando usuários não autenticados para a página de login.

---

## 4. Classe e Função para Usuário

```python
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
```

- A classe `User` representa um usuário autenticado.
- A função `load_user` permite carregar informações do usuário baseado no `user_id` armazenado na sessão.

---

## 5. Função para Conexão com Banco de Dados

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'gestao_tempo'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
```

- Configuração do banco MySQL e função que retorna conexão ativa para operações SQL.

---

## 6. Rotas Principais e Funcionalidades

### Login

- Recebe email e senha do formulário.
- Verifica no banco se o usuário existe.
- Se válido, inicia sessão e redireciona para página inicial.

### Cadastro

- Recebe dados do formulário para criar usuário.
- Valida presença e coerência dos dados.
- Insere novo usuário e inicia sessão automaticamente.

### CRUD Matérias e Tarefas

- Funções para adicionar, listar, editar, deletar matérias e tarefas.
- Cada rota faz validação de autenticação (`@login_required`).
- Manipulação de uploads de fotos com segurança.

### Manipulação de Tarefas com Datas

- Conversão e validação de prazo da tarefa, não permitindo datas passadas.
- Atualização de status da tarefa (pendente/concluída).

### APIs para Frontend

- Rotas que retornam JSON para alimentar elementos como calendário interativo (FullCalendar).

---

## 7. Uploads Seguros

```python
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
```

- Verifica se o arquivo enviado tem extensão permitida antes de salvar.

---

## 8. Execução da Aplicação

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

- Inicializa o servidor Flask, escutando em todas as interfaces na porta 5001 com modo debug ativo.

---

# Dicas para Apresentação

- Explique o uso das principais bibliotecas e suas funções.
- Mostre fluxo de autenticação e controle de sessão com flask-login.
- Destaque o uso do banco MySQL via mysql-connector e como as operações CRUD são feitas.
- Comente a importância das validações, segurança nos uploads e manipulação de datas.
- Mostre o uso das APIs JSON para frontend dinâmico (calendário).
- Enfatize organização do código em rotas e proteção com decoradores.

Esse guia ajudará no domínio do código para exposição técnica e tirar dúvidas durante a apresentação.

---
