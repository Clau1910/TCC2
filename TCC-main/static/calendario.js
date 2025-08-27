// Script para o calendário Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const calendarHeader = document.getElementById('calendar-header');
    const calendarDays = document.getElementById('calendar-days');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const currentMonthEl = document.getElementById('current-month');
    
    // Data atual
    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();
    
    // Inicializar o calendário
    function initCalendar() {
        updateCalendarHeader();
        generateCalendarDays();
        loadEvents();
        setupEventListeners();
    }
    
    // Atualizar cabeçalho do calendário
    function updateCalendarHeader() {
        const monthNames = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        
        currentMonthEl.textContent = `${monthNames[currentMonth]} ${currentYear}`;
    }
    
    // Gerar dias do calendário
    function generateCalendarDays() {
        calendarDays.innerHTML = '';
        
        // Primeiro dia do mês
        const firstDay = new Date(currentYear, currentMonth, 1);
        // Último dia do mês
        const lastDay = new Date(currentYear, currentMonth + 1, 0);
        // Dia da semana do primeiro dia (0 = Domingo, 1 = Segunda, etc.)
        const firstDayIndex = firstDay.getDay();
        // Dias no mês
        const daysInMonth = lastDay.getDate();
        
        // Dias do mês anterior
        const prevMonthLastDay = new Date(currentYear, currentMonth, 0).getDate();
        
        // Dias da semana
        const weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        
        // Gerar dias do mês anterior (se necessário)
        for (let i = firstDayIndex; i > 0; i--) {
            const day = prevMonthLastDay - i + 1;
            const dayElement = createDayElement(day, 'outro-mes');
            calendarDays.appendChild(dayElement);
        }
        
        // Gerar dias do mês atual
        const today = new Date();
        for (let i = 1; i <= daysInMonth; i++) {
            const isToday = i === today.getDate() && 
                           currentMonth === today.getMonth() && 
                           currentYear === today.getFullYear();
            
            const dayElement = createDayElement(i, isToday ? 'today' : '');
            calendarDays.appendChild(dayElement);
        }
        
        // Calcular dias restantes para completar a grade (42 células no total)
        const totalCells = 42;
        const remainingCells = totalCells - (firstDayIndex + daysInMonth);
        
        // Gerar dias do próximo mês
        for (let i = 1; i <= remainingCells; i++) {
            const dayElement = createDayElement(i, 'outro-mes');
            calendarDays.appendChild(dayElement);
        }
    }
    
    // Criar elemento de dia
    function createDayElement(day, className) {
        const dayElement = document.createElement('div');
        dayElement.className = `calendar-day ${className}`;
        
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        
        const eventsContainer = document.createElement('div');
        eventsContainer.className = 'day-events';
        
        const eventIndicator = document.createElement('div');
        eventIndicator.className = 'event-indicator';
        
        dayElement.appendChild(dayNumber);
        dayElement.appendChild(eventsContainer);
        dayElement.appendChild(eventIndicator);
        
        // Adicionar evento de clique
        dayElement.addEventListener('click', function() {
            showDayEvents(day, currentMonth + 1, currentYear);
        });
        
        return dayElement;
    }
    
    // Carregar eventos (simulação - substituir por chamada à API)
    function loadEvents() {
        // Simulação de eventos - substituir por chamada à API real
        const events = [
            { title: 'Reunião de Projeto', date: '2024-01-15', color: '#1a73e8' },
            { title: 'Entrega TCC', date: '2024-01-20', color: '#34a853' },
            { title: 'Apresentação', date: '2024-01-25', color: '#fbbc04' }
        ];
        
        events.forEach(event => {
            addEventToCalendar(event);
        });
    }
    
    // Adicionar evento ao calendário
    function addEventToCalendar(event) {
        const eventDate = new Date(event.date);
        if (eventDate.getMonth() === currentMonth && eventDate.getFullYear() === currentYear) {
            const dayElements = document.querySelectorAll('.calendar-day');
            const targetDay = eventDate.getDate();
            
            dayElements.forEach(dayElement => {
                const dayNumber = dayElement.querySelector('.day-number');
                if (dayNumber && parseInt(dayNumber.textContent) === targetDay) {
                    dayElement.classList.add('has-events');
                    
                    const eventElement = document.createElement('div');
                    eventElement.className = 'calendar-event';
                    eventElement.textContent = event.title;
                    eventElement.title = event.title;
                    eventElement.style.borderLeftColor = event.color;
                    eventElement.style.backgroundColor = event.color + '20'; // 20% de opacidade
                    
                    const eventsContainer = dayElement.querySelector('.day-events');
                    eventsContainer.appendChild(eventElement);
                }
            });
        }
    }
    
    // Mostrar eventos do dia (modal ou detalhes)
    function showDayEvents(day, month, year) {
        const formattedDate = `${day.toString().padStart(2, '0')}/${(month).toString().padStart(2, '0')}/${year}`;
        alert(`Eventos para ${formattedDate}\n\nEsta funcionalidade será implementada com um modal detalhado.`);
    }
    
    // Navegação entre meses
    function navigateMonth(direction) {
        if (direction === 'prev') {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
        } else {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
        }
        
        updateCalendarHeader();
        generateCalendarDays();
        loadEvents();
    }
    
    // Configurar event listeners
    function setupEventListeners() {
        prevMonthBtn.addEventListener('click', () => navigateMonth('prev'));
        nextMonthBtn.addEventListener('click', () => navigateMonth('next'));
        
        // Teclado: setas para navegar entre meses
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                navigateMonth('prev');
            } else if (e.key === 'ArrowRight') {
                navigateMonth('next');
            }
        });
    }
    
    // Inicializar o calendário
    initCalendar();
    
    // Função para adicionar evento via API (para uso externo)
    window.addCalendarEvent = function(eventData) {
        addEventToCalendar(eventData);
    };
    
    // Função para limpar eventos (para uso externo)
    window.clearCalendarEvents = function() {
        const eventElements = document.querySelectorAll('.calendar-event');
        eventElements.forEach(event => event.remove());
        
        const dayElements = document.querySelectorAll('.calendar-day');
        dayElements.forEach(day => day.classList.remove('has-events'));
    };
    
    // Função para atualizar calendário com novos eventos
    window.updateCalendarWithEvents = function(events) {
        window.clearCalendarEvents();
        events.forEach(event => addEventToCalendar(event));
    };
});

// Integração com a API existente
function loadTarefasFromAPI() {
    fetch('/tarefas_events')
        .then(response => response.json())
        .then(events => {
            const formattedEvents = events.map(event => ({
                title: event.title,
                date: event.start,
                color: getEventColorByClassName(event.className)
            }));
            
            if (typeof updateCalendarWithEvents === 'function') {
                updateCalendarWithEvents(formattedEvents);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar tarefas:', error);
        });
}

// Mapear classes CSS para cores
function getEventColorByClassName(className) {
    const colorMap = {
        'evento-pendente': '#ffc107',
        'evento-atrasada': '#dc3545',
        'evento-concluida': '#28a745',
        'evento-andamento': '#17a2b8',
        'evento-proxima': '#fd7e14'
    };
    
    return colorMap[className] || '#1a73e8';
}

// Carregar tarefas quando a página estiver pronta
document.addEventListener('DOMContentLoaded', function() {
    // Carregar tarefas após um pequeno delay para garantir que o calendário esteja inicializado
    setTimeout(loadTarefasFromAPI, 100);
});

// Notificações (exemplo)
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(notification, container.firstChild);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}
