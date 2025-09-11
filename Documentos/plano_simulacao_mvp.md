Plano de Simulação do MVP – Sistema de Gestão de Estudos
Tipo de MVP

Escolhemos o Single Feature MVP, pois o sistema já possui funcionalidades básicas implementadas e conectadas ao banco de dados. Dessa forma, é possível validar as interações principais do usuário antes de expandir para novas funções.

Cenários de Uso

Cadastro de Matéria

O estudante insere nome da disciplina, professor, horário e pode anexar uma imagem.

Os dados são salvos automaticamente no banco de dados e ficam disponíveis na lista de matérias.

Criação de Tarefa

O estudante cria uma tarefa vinculada a uma matéria existente, define prazo e descrição.

A tarefa é salva no banco de dados e aparece automaticamente no calendário.

Estrutura da Simulação

Usuário: estudante que interage diretamente com o sistema.

Produto (Sistema): o próprio sistema em funcionamento, já com banco de dados ativo.

Observador: responsável por acompanhar a execução, registrar feedbacks, dificuldades e sugestões de melhoria.

Exemplos de Diálogo

Cenário 1 – Cadastro de Matéria

Usuário: "Quero cadastrar a matéria Matemática, professor João, segundas e quartas, das 8h às 10h."

Sistema: "Matéria cadastrada com sucesso. Agora já aparece na sua lista de disciplinas."

Cenário 2 – Criação de Tarefa

Usuário: "Quero criar uma tarefa para Matemática: exercícios do capítulo 5, prazo 25/10."

Sistema: "Tarefa registrada com sucesso e adicionada ao calendário no dia 25/10."

Procedimentos

Definir os papéis de usuário e observador.

Realizar os testes diretamente no sistema.

Coletar feedbacks sobre clareza, usabilidade e tempo de resposta.

Reunir o grupo para analisar os resultados e propor melhorias futuras.