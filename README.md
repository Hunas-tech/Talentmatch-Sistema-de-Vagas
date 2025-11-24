TalentMatch - Plataforma de Recrutamento Inteligente (TCC)

⚠️ AVISO DE DESENVOLVIMENTO: Este projeto é um Trabalho de Conclusão de Curso (TCC) e está atualmente em fase ativa de desenvolvimento. Algumas funcionalidades podem estar incompletas, conter bugs ou não funcionar conforme o esperado. A estrutura do banco de dados e as rotas podem sofrer alterações sem aviso prévio.

📋 Sobre o Projeto

O TalentMatch é uma plataforma web desenvolvida em Django (Python) que visa conectar candidatos a oportunidades de emprego de forma eficiente. O sistema permite que empresas publiquem vagas e que candidatos se inscrevam, gerenciem seus perfis e acompanhem processos seletivos.

Funcionalidades Atuais (MVP)

Autenticação: Cadastro e Login seguros para Candidatos e Empresas.

Perfis: Criação automática de perfis de Candidato (com upload de currículo) e Empresa (com logo).

Vagas: Visualização de vagas ativas na página inicial.

Dashboard: Painéis administrativos básicos para candidatos e empresas.

Admin: Interface administrativa do Django para gerenciamento total do sistema.

🛠️ Tecnologias Utilizadas

Backend: Python 3.12+, Django 5.0

Banco de Dados: SQLite (Nativo do Django para desenvolvimento)

Frontend: HTML5, CSS3 (Design System próprio), JavaScript (básico)

Bibliotecas Principais: Pillow (processamento de imagens), python-dotenv (segurança).

🚀 Guia de Instalação e Execução

Siga estes passos estritamente para rodar o projeto em sua máquina local (Windows).

1. Pré-requisitos

Python 3.12 ou superior instalado.

Git (opcional, para clonar o repositório).

2. Configuração do Ambiente (Terminal)

Abra o seu terminal (PowerShell ou CMD) na pasta raiz do projeto.

Crie o Ambiente Virtual:

python -m venv venv


Ative o Ambiente:

.\venv\Scripts\activate


(Você deve ver (venv) no início da linha do terminal).

Instale as Dependências:

pip install django pillow python-dotenv


3. Configuração do Banco de Dados

Como estamos usando SQLite, não é necessário instalar nenhum banco de dados externo. Apenas rode as migrações para criar o arquivo db.sqlite3.

Entre na pasta do projeto (onde está o manage.py):

cd projeto_tcc 
# (verifique o nome da sua pasta)


Crie as Migrações do App Principal:

python manage.py makemigrations core


Aplique as Migrações (Construir o Banco):

python manage.py migrate


Crie um Superusuário (Admin):

python manage.py createsuperuser


(Siga as instruções na tela para criar login, email e senha).

4. Executando o Projeto

Inicie o Servidor:

python manage.py runserver


Acesse no Navegador:

Site Principal: http://127.0.0.1:8000/

Painel Administrativo: http://127.0.0.1:8000/admin/

📂 Estrutura de Pastas

TCC/
├── venv/                   # Ambiente Virtual (Bibliotecas)
├── projeto_tcc/            # Pasta do Projeto Django
│   ├── manage.py           # Gerenciador de comandos
│   ├── db.sqlite3          # Banco de Dados (arquivo único)
│   ├── projeto_tcc/        # Configurações Globais (settings.py, urls.py)
│   ├── core/               # App Principal (models.py, views.py)
│   ├── templates/          # Arquivos HTML
│   ├── static/             # CSS, JS e Imagens do site
│   └── media/              # Uploads de usuários (currículos, logos)
└── README.md               # Este arquivo


⚠️ Problemas Conhecidos

O layout pode apresentar inconsistências em dispositivos móveis.

O sistema de "match" com IA ainda não está implementado.

Algumas páginas do dashboard podem conter dados estáticos (mockup) em vez de dados reais do banco.

Trabalho de Conclusão de Curso - 2025
