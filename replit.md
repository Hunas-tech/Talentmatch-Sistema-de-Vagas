# TalentMatch - Sistema de Recrutamento Inteligente

## 📋 Visão Geral

O **TalentMatch** é uma plataforma web desenvolvida em **Django (Python)** que conecta candidatos a oportunidades de emprego de forma eficiente e inteligente. Este projeto é um Trabalho de Conclusão de Curso (TCC) desenvolvido no SENAI.

## 🏗️ Estrutura do Projeto

```
PROJETO_RAIZ/
├── core/                           # App principal Django
│   ├── management/                 # Comandos personalizados
│   │   └── commands/
│   │       ├── criar_dados_exemplo.py  # Cria dados de exemplo
│   │       └── __init__.py
│   ├── migrations/                 # Migrações do banco de dados
│   │   ├── 0001_initial.py
│   │   ├── 0002_notificacao.py
│   │   ├── 0003_mensagem_match_candidatura.py
│   │   └── __init__.py
│   ├── templatetags/              # Tags personalizadas do Django
│   │   ├── user_tags.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                   # Configuração do Django Admin
│   ├── apps.py                    # Configuração do app
│   ├── context_processors.py      # Processadores de contexto
│   ├── forms.py                   # Formulários Django
│   ├── matching.py                # Algoritmo de matching de vagas
│   ├── models.py                  # Models do banco de dados
│   ├── signals.py                 # Sinais Django (notificações)
│   ├── tests.py                   # Testes unitários
│   ├── urls.py                    # Rotas do app
│   └── views.py                   # Views (lógica das páginas)
│
├── talentmatch_project/           # Configuração do projeto Django
│   ├── __init__.py
│   ├── asgi.py                   # Configuração ASGI
│   ├── settings.py               # Configurações principais
│   ├── urls.py                   # Rotas principais
│   └── wsgi.py                   # Configuração WSGI
│
├── templates/                     # Templates HTML organizados por área
│   ├── auth/                     # Autenticação
│   │   ├── login.html
│   │   ├── cadastro.html
│   │   └── cadastro_empresa.html
│   │
│   ├── candidate/                # Área do Candidato
│   │   ├── dashboard_candidato.html
│   │   ├── perfil_candidato.html
│   │   ├── editar_perfil_candidato.html
│   │   ├── explorar_vagas.html
│   │   ├── detalhe_vaga.html
│   │   ├── candidaturas_vagas.html
│   │   ├── cursos.html
│   │   ├── progre_cursos.html
│   │   ├── chat_ia.html
│   │   ├── mensagens.html
│   │   └── analise.html
│   │
│   ├── company/                  # Área da Empresa
│   │   ├── dashboard_empresa.html
│   │   ├── perfil_empresa.html
│   │   ├── editar_perfil_empresa.html
│   │   ├── cadastrar_vaga.html
│   │   └── editar_vaga.html
│   │
│   ├── admin_panel/              # Painel Administrativo
│   │   ├── dashboard_admin.html
│   │   ├── gerenciar_usuarios.html
│   │   ├── gerenciar_empresas.html
│   │   ├── gerenciar_vagas.html
│   │   ├── admin_confirmar_deletar_candidato.html
│   │   ├── admin_confirmar_deletar_empresa.html
│   │   ├── admin_confirmar_deletar_vaga.html
│   │   ├── painel_denuncias.html
│   │   ├── painel_denuncias_resolvidas.html
│   │   ├── painel_denuncias_ignoradas.html
│   │   ├── relatorios.html
│   │   └── config_admin.html
│   │
│   ├── base.html                 # Template base
│   ├── landing.html              # Página inicial pública
│   ├── conf.html                 # Configurações do usuário
│   ├── sair.html                 # Página de logout
│   ├── confirmar_cancelar_candidatura.html
│   └── confirmar_deletar_vaga.html
│
├── static/                       # Arquivos estáticos (CSS, JS)
│   └── css/
│       └── styles.css
│
├── media/                        # Uploads de usuários
│   ├── curriculos/              # Currículos dos candidatos
│   └── logos/                   # Logos das empresas
│
├── manage.py                    # Gerenciador Django
├── pyproject.toml               # Dependências do projeto
├── db.sqlite3                   # Banco de dados SQLite
├── README.md                    # Documentação original
├── CONFIGURACAO_CHAT_IA.md      # Instruções para configurar chat IA
└── replit.md                    # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.12+**
- **Django 5.2** - Framework web principal
- **SQLite** - Banco de dados (desenvolvimento)
- **Pillow** - Processamento de imagens
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **OpenAI API** - Chat IA inteligente
- **Gunicorn** - Servidor WSGI para produção
- **psycopg2-binary** - Suporte PostgreSQL
- **dj-database-url** - Configuração de banco de dados via URL

### Frontend
- **HTML5**
- **CSS3** (Design System customizado)
- **Tailwind CSS** (via CDN)
- **JavaScript** (vanilla)

## ⚙️ Funcionalidades Implementadas

### ✅ Autenticação e Perfis
- Cadastro de Candidatos e Empresas
- Login e Logout seguros
- Gestão de perfis com upload de currículo e logo
- Perfis personalizados por tipo de usuário

### 💼 Sistema de Vagas
- Cadastro e edição de vagas (Empresas)
- Exploração de vagas com filtros
- Detalhamento de vagas
- Sistema de candidaturas
- Status de vagas (aberta/fechada)

### 🎯 Matching Inteligente
- Algoritmo de compatibilidade candidato-vaga
- Cálculo de score baseado em:
  - Habilidades (40%)
  - Experiência (25%)
  - Localização (20%)
  - Salário (15%)
- Geração automática de matches

### 📬 Comunicação
- Sistema de mensagens entre usuários
- Notificações em tempo real
- Chat IA para assistência aos candidatos
- Integração com OpenAI API

### 🎓 Cursos e Desenvolvimento
- Listagem de cursos disponíveis
- Acompanhamento de progresso

### 👨‍💼 Painel Administrativo
- Gerenciamento de usuários
- Gerenciamento de empresas
- Gerenciamento de vagas
- Painel de denúncias
- Relatórios e estatísticas

## 🚀 Como Executar o Projeto

### O servidor Django já está configurado e rodando!

O projeto está configurado para executar automaticamente. Você pode acessar:

- **Site Principal**: Clique no botão "Webview" no topo
- **Painel Admin**: `/gerenciador/` (requer superusuário)

### Criar Superusuário (Admin)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar um usuário admin.

### Criar Dados de Exemplo

```bash
python manage.py criar_dados_exemplo
```

Este comando cria:
- Usuários de exemplo
- Candidatos
- Empresas
- Vagas
- Matches

### Comandos Úteis

```bash
# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Limpar banco de dados e recriar
python manage.py flush

# Executar shell Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

## 📊 Modelos do Banco de Dados

### User (Django Auth)
- Usuário base do Django
- Campos: username, email, password, is_staff, is_superuser

### Candidato
- Perfil estendido do candidato
- Campos: user, nome_completo, telefone, cidade, estado, habilidades, experiencia, curriculo, etc.

### Empresa
- Perfil estendido da empresa
- Campos: user, nome_empresa, cnpj, telefone, endereco, logo, etc.

### Vaga
- Vagas criadas pelas empresas
- Campos: empresa, titulo, descricao, tipo, nivel, salario, cidade, status, etc.

### Match
- Relacionamento candidato-vaga com score
- Campos: candidato, vaga, score, candidato_interessado, empresa_interessada

### Candidatura
- Candidaturas formais dos candidatos
- Campos: candidato, vaga, status, data_aplicacao

### Notificacao
- Sistema de notificações
- Campos: usuario, tipo, mensagem, lida, criado_em

### Mensagem
- Sistema de mensagens entre usuários
- Campos: remetente, destinatario, assunto, conteudo, lida

### Curso e ProgressoCurso
- Sistema de cursos e acompanhamento de progresso

## 🔧 Configurações Importantes

### settings.py
- `DEBUG = True` (apenas desenvolvimento)
- `ALLOWED_HOSTS = ['*']`
- `LANGUAGE_CODE = 'pt-br'`
- `TIME_ZONE = 'America/Sao_Paulo'`
- Templates configurados em `templates/`
- Static files em `static/`
- Media files em `media/`

### Algoritmo de Matching
Os pesos podem ser ajustados em `settings.py`:

```python
MATCHING_WEIGHTS = {
    'habilidades': 40,
    'experiencia': 25,
    'localizacao': 20,
    'salario': 15,
}
```

## 🔐 Variáveis de Ambiente (Opcionais)

Para usar o Chat IA, configure:
- `OPENAI_API_KEY` - Chave da API OpenAI

Ver `CONFIGURACAO_CHAT_IA.md` para mais detalhes.

## 📝 Rotas Principais

### Públicas
- `/` - Landing page
- `/login/` - Login
- `/cadastro/` - Cadastro de candidato
- `/cadastro_empresa/` - Cadastro de empresa

### Candidato (requer login)
- `/dashboard_candidato/` - Dashboard
- `/perfil/` - Perfil do candidato
- `/editar-perfil/` - Editar perfil
- `/vagas/` - Explorar vagas
- `/candidaturas/` - Minhas candidaturas
- `/cursos/` - Cursos disponíveis
- `/mensagens/` - Caixa de mensagens
- `/chat_ia/` - Chat com IA

### Empresa (requer login)
- `/dashboard_empresa/` - Dashboard
- `/empresa/perfil/` - Perfil da empresa
- `/empresa/editar-perfil/` - Editar perfil
- `/cadastrar_vaga/` - Cadastrar vaga
- `/empresa/candidaturas/` - Candidaturas recebidas

### Admin (requer is_staff)
- `/dashboard_admin/` - Dashboard administrativo
- `/gerenciar_usuarios/` - Gerenciar usuários
- `/gerenciar_empresas/` - Gerenciar empresas
- `/gerenciar_vagas/` - Gerenciar vagas
- `/painel_denuncias/` - Painel de denúncias
- `/relatorios/` - Relatórios

### API
- `/api/matches/candidato/<id>/` - Gerar matches para candidato
- `/api/matches/vaga/<id>/` - Gerar matches para vaga
- `/api/vaga/<id>/aplicar/` - Aplicar para vaga
- `/api/meus-matches/` - Listar meus matches
- `/api/chat/ia/` - Chat com IA
- `/api/notificacoes/` - Listar notificações

## 🐛 Solução de Problemas

### Erro de Template não encontrado
- Verifique se o template está na pasta correta em `templates/`
- Verifique se o caminho no `render()` está correto

### Erro de Static Files
- Execute `python manage.py collectstatic`
- Verifique `STATIC_URL` e `STATICFILES_DIRS` em settings.py

### Erro de Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Resetar Banco de Dados
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py criar_dados_exemplo
```

## 📚 Estrutura de Código

### views.py
Organizado em seções:
- Funções auxiliares
- Páginas gerais
- Área do candidato
- Área da empresa
- Área administrativa
- APIs

### models.py
Todos os modelos do banco de dados

### forms.py
Formulários Django para edição de perfis e vagas

### matching.py
Algoritmo inteligente de matching

### signals.py
Sinais para criação automática de notificações

## 🎨 Design e UI

- Design System customizado em `static/css/styles.css`
- Tailwind CSS para componentes rápidos
- Layout responsivo
- Template base com navegação dinâmica

## ⚠️ Avisos Importantes

- Este é um projeto em desenvolvimento (TCC)
- Não usar em produção sem configurações de segurança adicionais
- O Tailwind CDN não deve ser usado em produção
- Configurar `DEBUG = False` e `SECRET_KEY` adequada para produção
- Usar PostgreSQL ou MySQL em produção (não SQLite)

## 📄 Licença

Projeto desenvolvido para fins educacionais - TCC SENAI 2025

## 👥 Contribuidores

- Thiago Hunas
- Alef Santos
- Gabriel Pedro
- Thiagoolivs

---

**Última Atualização**: Novembro 2024
**Django Version**: 5.2.8
**Python Version**: 3.12+
