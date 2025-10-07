## TODO - Implementar Funcionalidade de Marcar Tarefas como Concluídas

### 1. Atualizar TarefaObj em main.py
- [x] Definir self.concluida = (self.status == 'concluída') na classe TarefaObj

### 2. Adicionar Rota de Toggle em main.py
- [x] Criar rota /toggle_status/<int:id_tarefa> que alterna status entre 'pendente' e 'concluída'

### 3. Atualizar list_tarefas.html
- [x] Adicionar botão "Marcar como Concluída" ou "Marcar como Pendente" no card-footer

### 4. Atualizar list_tarefas_materia.html
- [x] Adicionar botão similar para toggle de status

### 5. Testes
- [x] Testar toggle de status via interface
- [x] Verificar atualização da barra de progresso
- [x] Verificar badges e status nos cards
