# TODO - Implementação de Calendário Dinâmico com Sistema de Cores

## Funcionalidades Principais:
- [x] Calendário de 12 meses com visualização anual ✅
- [x] Sistema de cores baseado no status das tarefas: ✅
  - 🟡 Amarelo: Tarefas pendentes
  - 🔴 Vermelho: Tarefas atrasadas  
  - 🟢 Verde: Tarefas concluídas
  - 🔵 Azul: Tarefas em andamento
  - 🟠 Laranja: Tarefas próximas do prazo
- [x] Sino de notificação para tarefas próximas do prazo ✅
- [x] Carregamento dinâmico dos dados do banco ✅

## Implementações Concluídas:

### Backend (main.py)
- [x] Atualizada rota `/tarefas_events` para incluir campo `status`
- [x] Implementada função `determinar_cor_tarefa()` para sistema de cores
- [x] Lógica para identificar tarefas atrasadas e próximas do prazo

### Frontend (calendario.html)
- [x] Configurado FullCalendar para visualização anual
- [x] Implementado carregamento dinâmico via AJAX
- [x] Adicionado sistema de notificações com sino
- [x] Eventos coloridos baseados no status

### CSS (calendario.css)
- [x] Definidas classes CSS para cada status de tarefa
- [x] Estilizado sistema de notificações
- [x] Indicadores visuais nos eventos

## Próximos Passos:
- [ ] Testar integração com banco de dados
- [ ] Implementar modal de detalhes completo
- [ ] Adicionar filtros funcionais por matéria
- [ ] Testar sistema de notificações

## Progresso:
- [x] Backend implementado ✅
- [x] Frontend implementado ✅  
- [x] CSS atualizado ✅
- [ ] Testes de integração
- [ ] Refinamentos finais
