# Documento de Casos de Uso - Sistema de Gestão de Estudos

Este documento descreve os casos de uso principais do Sistema de Gestão de Estudos, uma aplicação web para organização acadêmica. Inclui diagramas de casos de uso (disponível em `diagrama_casos_uso.drawio`) e descrições detalhadas de cada caso de uso selecionado.

## Diagrama de Casos de Uso

O diagrama geral está disponível no arquivo `diagrama_casos_uso.drawio`, que pode ser aberto no draw.io para visualização ou edição. Ele mostra o ator "Usuário" interagindo com 17 casos de uso agrupados por funcionalidades (autenticação, matérias, tarefas, calendário).

## Descrições dos Casos de Uso

Abaixo, descrições detalhadas dos casos de uso principais. Cada um inclui nome, autor, data, descrição, atores, pré/pós-condições e cenários.

### 1. Fazer Login

**Nome:** Fazer Login  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Permite ao usuário autenticar-se no sistema para acessar suas funcionalidades pessoais.  

**Atores envolvidos:** Usuário  

**Pré-condições:**  
- O usuário deve ter uma conta cadastrada no sistema.  
- O navegador deve estar conectado à internet.  

**Pós-condições:**  
- O usuário é redirecionado para a página inicial se o login for bem-sucedido.  
- Uma sessão é iniciada para o usuário.  

**Cenário normal:**  
1. O usuário acessa a página de login.  
2. Insere email e senha.  
3. Clica em "Entrar".  
4. O sistema valida as credenciais no banco de dados.  
5. Se válidas, o usuário é logado e redirecionado.  

**Cenário alternativo:**  
- Se as credenciais forem inválidas, exibe mensagem de erro e permanece na página de login.  

### 2. Fazer Cadastro

**Nome:** Fazer Cadastro  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Permite ao novo usuário criar uma conta no sistema.  

**Atores envolvidos:** Usuário  

**Pré-condições:**  
- O email não deve estar cadastrado.  
- O navegador deve estar conectado.  

**Pós-condições:**  
- Uma nova conta é criada no banco de dados.  
- O usuário é automaticamente logado.  

**Cenário normal:**  
1. O usuário acessa a página de cadastro.  
2. Preenche nome, email, senha e confirmação.  
3. Clica em "Cadastrar".  
4. O sistema valida os dados (senha >=6 caracteres, emails iguais).  
5. Insere no banco e loga o usuário.  

**Cenário alternativo:**  
- Se email já existir ou validação falhar, exibe erro e permanece na página.  

### 3. Adicionar Matéria

**Nome:** Adicionar Matéria  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Permite ao usuário cadastrar uma nova matéria com detalhes e foto opcional.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- O usuário deve estar logado.  
- Conexão com banco de dados ativa.  

**Pós-condições:**  
- A matéria é salva no banco com foto (se enviada).  
- O usuário é redirecionado para a lista de matérias.  

**Cenário normal:**  
1. O usuário acessa a página de adicionar matéria.  
2. Preenche nome, professor, horário e seleciona foto.  
3. Clica em "Adicionar".  
4. O sistema valida campos obrigatórios.  
5. Salva no banco e redireciona.  

**Cenário alternativo:**  
- Se foto inválida, usa padrão; se erro de DB, exibe mensagem.  

### 4. Listar Matérias

**Nome:** Listar Matérias  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Exibe todas as matérias do usuário logado.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Usuário logado.  

**Pós-condições:**  
- Lista de matérias é exibida.  

**Cenário normal:**  
1. O usuário acessa a página de listagem.  
2. O sistema consulta matérias do usuário.  
3. Renderiza a lista com fotos e ações (editar/deletar).  

**Cenário alternativo:**  
- Se nenhuma matéria, exibe mensagem vazia.  

### 5. Adicionar Tarefa

**Nome:** Adicionar Tarefa  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Permite criar uma tarefa vinculada a uma matéria.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Usuário logado; pelo menos uma matéria cadastrada.  

**Pós-condições:**  
- Tarefa salva no banco.  

**Cenário normal:**  
1. Acessa página de adicionar tarefa.  
2. Seleciona matéria, preenche título, descrição, prazo.  
3. Clica em "Adicionar".  
4. Valida data futura e campos.  
5. Salva e redireciona.  

**Cenário alternativo:**  
- Data passada: erro; matéria inválida: erro.  

### 6. Listar Tarefas

**Nome:** Listar Tarefas  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Exibe tarefas do usuário com status e ações.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Usuário logado.  

**Pós-condições:**  
- Lista renderizada.  

**Cenário normal:**  
1. Acessa listagem.  
2. Sistema consulta tarefas.  
3. Exibe com botões para editar/deletar/toggle status.  

**Cenário alternativo:**  
- Lista vazia se nenhuma tarefa.  

### 7. Visualizar Calendário

**Nome:** Visualizar Calendário  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Mostra calendário interativo com tarefas como eventos.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Usuário logado.  

**Pós-condições:**  
- Calendário carregado com eventos.  

**Cenário normal:**  
1. Acessa página de calendário.  
2. Sistema carrega eventos via API.  
3. FullCalendar renderiza com cores por status.  

**Cenário alternativo:**  
- Sem tarefas: calendário vazio.  

### 8. Upload Foto Tarefa

**Nome:** Upload Foto Tarefa  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Permite anexar foto a uma tarefa existente.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Tarefa existente.  

**Pós-condições:**  
- Foto salva e vinculada.  

**Cenário normal:**  
1. Na edição de tarefa, seleciona foto.  
2. Envia.  
3. Sistema salva arquivo e registra no banco.  

**Cenário alternativo:**  
- Arquivo inválido: erro.  

### 9. Alterar Status Tarefa

**Nome:** Alterar Status Tarefa  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Marca tarefa como concluída ou pendente.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Tarefa pendente.  

**Pós-condições:**  
- Status atualizado.  

**Cenário normal:**  
1. Clica em botão de toggle na lista.  
2. Sistema atualiza status para concluída.  

**Cenário alternativo:**  
- Já concluída: permanece.  

### 10. Fazer Logout

**Nome:** Fazer Logout  
**Autor:** Sistema de Gestão de Estudos  
**Data:** 01/10/2023  

**Descrição:** Encerra a sessão do usuário.  

**Atores envolvidos:** Usuário (logado)  

**Pré-condições:**  
- Sessão ativa.  

**Pós-condições:**  
- Sessão destruída; redirecionado para login.  

**Cenário normal:**  
1. Clica em logout.  
2. Sistema limpa sessão e redireciona.  

**Cenário alternativo:**  
- Nenhum.  

Este documento cobre os casos de uso essenciais. Para mais detalhes ou adições, consulte o código fonte ou diagramas.
