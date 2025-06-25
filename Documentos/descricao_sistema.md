# Descrição do Sistema de Gestão de Estudos

Este sistema é uma aplicação web desenvolvida em Python utilizando o framework Flask, com o objetivo de auxiliar estudantes na organização e gestão de seus estudos. Através dele, o usuário pode cadastrar, editar e acompanhar suas matérias e tarefas, facilitando o planejamento e o controle do tempo dedicado a cada atividade acadêmica.

## Principais funcionalidades

- **Autenticação de usuários:** permite login e logout, garantindo que cada usuário tenha acesso exclusivo aos seus dados.
- **Cadastro e gerenciamento de matérias:** o usuário pode adicionar informações sobre suas matérias, incluindo nome, professor, horário e uma foto ilustrativa.
- **Cadastro e gerenciamento de tarefas:** é possível criar, editar e excluir tarefas relacionadas às matérias, com descrição detalhada e prazo de entrega.
- **Upload e visualização de fotos:** o sistema permite anexar fotos tanto às matérias quanto às tarefas, enriquecendo a organização visual.
- **Integração com calendário:** as tarefas são exibidas em um calendário interativo (FullCalendar), facilitando a visualização dos prazos e eventos.
- **Armazenamento em banco de dados MySQL:** todas as informações são persistidas em um banco de dados relacional, garantindo segurança e integridade dos dados.

## Tecnologias utilizadas

- Python e Flask para o backend e lógica da aplicação.
- MySQL para gerenciamento do banco de dados.
- HTML, CSS e JavaScript para a interface web, incluindo templates Jinja2 para renderização dinâmica.
- Flask-Login para gerenciamento de sessões e autenticação.
- Biblioteca FullCalendar para exibição do calendário de tarefas.

## Bibliotecas Python utilizadas

- **flask:** micro framework web para criação da aplicação.
- **gunicorn:** servidor HTTP para aplicações Python WSGI, usado em produção.
- **flask-sqlalchemy:** extensão para facilitar o uso do ORM SQLAlchemy.
- **mysql-connector-python:** conector oficial para comunicação com banco MySQL.
- **flask-login:** extensão para autenticação e gerenciamento de sessões.

## Bibliotecas JavaScript utilizadas

- **FullCalendar:** criação de calendários interativos e visualização de eventos.
- **Axios:** requisições HTTP assíncronas para comunicação com APIs.
- **Flatpickr:** seletor de datas leve e personalizável para inputs.
- **Luxon:** manipulação e formatação avançada de datas e horários.

## Objetivo do sistema

Este sistema visa proporcionar uma ferramenta prática e eficiente para estudantes melhorarem sua organização acadêmica, otimizando o tempo e facilitando o acompanhamento das atividades escolares.
