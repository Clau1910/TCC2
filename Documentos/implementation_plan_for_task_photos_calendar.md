Plano Detalhado para Implementação do Upload e Exibição de Fotos das Tarefas no Calendário

1. Objetivo
Implementar o upload, armazenamento, listagem e exclusão de fotos associadas às tarefas, e integrar a exibição dessas fotos no calendário, conforme o escopo definido.

2. Banco de Dados
- Utilizar a tabela atividades_fotos para armazenar os nomes dos arquivos das fotos associadas às tarefas.
- Garantir que as relações com tarefas e usuários estejam corretas.

3. Backend (TCC-main/main.py)
- Criar rota para upload de fotos das tarefas:
  - Receber arquivo via formulário.
  - Validar extensão e salvar na pasta static/uploads.
  - Inserir registro na tabela atividades_fotos com tarefa_id, usuario_id e nome do arquivo.
- Criar rota para listar fotos de uma tarefa específica.
- Criar rota para exclusão de fotos.
- Ajustar rotas de listagem de tarefas para incluir as fotos associadas.
- Ajustar rotas do calendário para incluir dados das fotos.

4. Frontend (Templates)
- Atualizar template de criação/edição de tarefas para permitir upload de fotos.
- Atualizar template do calendário para exibir miniaturas das fotos das tarefas.
- Implementar modal ou página para exibir detalhes da tarefa e fotos ampliadas.
- Implementar filtro/seletor para escolher matéria e atualizar calendário dinamicamente.

5. Testes
- Testar upload, listagem e exclusão das fotos das tarefas.
- Testar exibição das fotos no calendário, tanto no modo geral quanto filtrado por matéria.
- Testar fluxo completo de criação, edição e exclusão de tarefas com fotos.

6. Dependências
- Verificar se há necessidade de bibliotecas adicionais para upload e manipulação de imagens.

7. Cronograma
- Planejar a implementação em etapas, começando pelo backend, seguido do frontend e testes.

Após aprovação deste plano, iniciarei a implementação conforme descrito.
