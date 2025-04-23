USE gestao_tempo;

INSERT INTO usuarios (id, nome, email, senha) VALUES
(1, 'Usuário Padrão', 'usuario@exemplo.com', 'senha123')
ON DUPLICATE KEY UPDATE nome=VALUES(nome), email=VALUES(email), senha=VALUES(senha);
