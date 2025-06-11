CREATE DATABASE IF NOT EXISTS gestao_tempo;
USE gestao_tempo;

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(80) UNIQUE NOT NULL,
    senha VARCHAR(12) NOT NULL
);

-- Tabela de Matérias
CREATE TABLE IF NOT EXISTS materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    professor VARCHAR(50),
    horario TIME,
    foto VARCHAR(100),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela de Tarefas
CREATE TABLE IF NOT EXISTS tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    materia_id INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT,
    prazo DATE,
    status ENUM('pendente', 'em andamento', 'concluída') DEFAULT 'pendente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
);

-- Tabela para Upload de Fotos de Atividades
CREATE TABLE IF NOT EXISTS atividades_fotos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tarefa_id INT NOT NULL,
    foto VARCHAR(100) NOT NULL,
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE
);

-- Tabela de Eventos do Calendário
CREATE TABLE IF NOT EXISTS calendario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    titulo VARCHAR(50) NOT NULL,
    descricao TEXT,
    data_inicio DATETIME NOT NULL,
    data_fim DATETIME NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Inserção de usuário padrão
INSERT INTO usuarios (id, nome, email, senha) VALUES
(1, 'Usuário Padrão', 'usuario@exemplo.com', 'senha123')
ON DUPLICATE KEY UPDATE nome=VALUES(nome), email=VALUES(email), senha=VALUES(senha);

