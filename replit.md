# TalentMatch - Plataforma Inteligente de Matching de Vagas

## Visão Geral do Projeto
TalentMatch é uma plataforma web Django completa para matching inteligente entre candidatos e vagas de emprego. O sistema utiliza algoritmos de compatibilidade, IA para orientação de carreira e oferece uma interface intuitiva e interativa para candidatos, empresas e administradores.

## Tecnologias Utilizadas
- **Django**: 5.2.8
- **Python**: 3.11
- **Banco de Dados**: PostgreSQL (Neon-backed via DATABASE_URL)
- **IA**: OpenAI API (GPT-4o-mini) para chat inteligente
- **Frontend**: TailwindCSS via CDN
- **Idioma**: Português (pt-br)

## Funcionalidades Principais

### Para Candidatos
- ✅ **Cadastro e Login Completos**: Sistema de autenticação com validação de email e senha
- ✅ **Dashboard Personalizado**: Visualização de matches, vagas recomendadas e estatísticas
- ✅ **Perfil Detalhado**: Habilidades, experiência, escolaridade, pretensão salarial
- ✅ **Explorar Vagas**: Filtros por cidade, tipo (remoto/presencial/híbrido) e nível
- ✅ **Candidaturas**: Aplicar para vagas com score de compatibilidade em tempo real
- ✅ **Chat com IA**: Assistente virtual para orientação de carreira
- ✅ **Cursos**: Acesso a cursos com tracking de progresso
- ✅ **Mensagens**: Sistema interno de mensagens com empresas
- ✅ **Notificações**: Alertas de novos matches, vagas e mensagens

### Para Empresas
- ✅ **Cadastro com CNPJ**: Validação e registro de empresas
- ✅ **Dashboard Empresarial**: Estatísticas de vagas e candidatos
- ✅ **Cadastro de Vagas**: Criação de vagas com requisitos detalhados
- ✅ **Matches Automáticos**: Sistema gera automaticamente candidatos compatíveis
- ✅ **Gestão de Candidaturas**: Visualização de candidatos interessados

### Para Administradores
- ✅ **Dashboard Administrativo**: Estatísticas completas da plataforma
- ✅ **Gerenciar Usuários**: Listagem e busca de candidatos
- ✅ **Gerenciar Empresas**: Controle de empresas cadastradas
- ✅ **Gerenciar Vagas**: Filtros por status (aberta/fechada/pausada)
- ✅ **Relatórios**: Análise de dados da plataforma

## Arquitetura do Projeto

### Estrutura de Diretórios
```
talentmatch_project/
├── core/                    # App principal
│   ├── models.py           # Modelos do banco de dados
│   ├── views.py            # Views e APIs
│   ├── urls.py             # Rotas da aplicação
│   ├── matching.py         # Algoritmo de matching
│   ├── admin.py            # Configuração do Django Admin
│   └── migrations/         # Migrações do banco
├── talentmatch_project/    # Configuração do projeto
│   ├── settings.py         # Configurações Django
│   ├── urls.py             # URLs principais
│   └── wsgi.py             # Servidor WSGI
├── templates/              # Templates HTML
├── static/                 # Arquivos estáticos (CSS)
├── manage.py               # CLI do Django
└── pyproject.toml          # Dependências Python
```

### Modelos do Banco de Dados
1. **Candidato**: Perfil completo do candidato com habilidades, experiência, localização
2. **Empresa**: Dados da empresa (CNPJ, setor, descrição)
3. **Vaga**: Vagas com requisitos, habilidades, salário, tipo de trabalho
4. **Match**: Registro de compatibilidade candidato-vaga (score 0-100)
5. **Candidatura**: Sistema de candidaturas com status, carta de apresentação e observações
6. **Mensagem**: Sistema de mensagens entre usuários (com campo match opcional)
7. **Curso**: Catálogo de cursos disponíveis
8. **ProgressoCurso**: Acompanhamento de progresso em cursos
9. **Notificacao**: Sistema de alertas e notificações

## Algoritmo de Matching Inteligente

O sistema calcula um score de compatibilidade (0-100) baseado em:

### 1. Habilidades (40 pontos)
- Compara habilidades do candidato com as requeridas pela vaga
- Porcentagem de match convertida em pontos

### 2. Localização (20 pontos)
- Mesma cidade: 20 pontos
- Mesmo estado: 15 pontos
- Vaga remota: 20 pontos (localização irrelevante)
- Híbrido em outro estado: 5 pontos

### 3. Experiência (20 pontos)
- Atende requisito mínimo: 20 pontos
- 70% do requisito: 15 pontos
- 50% do requisito: 10 pontos
- Menos que 50%: 5 pontos

### 4. Salário (15 pontos)
- Pretensão dentro da faixa: 15 pontos
- Até 20% acima do máximo: 10 pontos
- Sem informação salarial: 8 pontos (neutro)

**Configuração de Pesos**:
Os pesos são configuráveis via `settings.MATCHING_WEIGHTS`:
```python
MATCHING_WEIGHTS = {
    'habilidades': 40,
    'experiencia': 25,
    'localizacao': 20,
    'salario': 15,
}
```
O sistema valida automaticamente os pesos e usa valores padrão se inválidos.

## APIs Disponíveis

### Matching e Candidaturas
- `GET /api/matches/candidato/<id>/` - Matches para um candidato
- `GET /api/matches/vaga/<id>/` - Candidatos compatíveis para uma vaga
- `POST /api/vagas/<vaga_id>/candidatar/` - Aplicar para uma vaga
  - Body (opcional): `{"carta_apresentacao": "..."}`
  - Retorna: `{"sucesso": true, "candidatura_id": 123, "status": "pendente"}`
- `POST /api/candidaturas/<id>/atualizar/` - Atualizar status de candidatura (empresa)
  - Body: `{"status": "aprovada", "observacoes": "..."}`
  - Status válidos: `pendente`, `em_analise`, `aprovada`, `recusada`
- `GET /api/meus-matches/` - Matches do candidato logado

### Chat IA
- `POST /api/chat/ia/` - Conversar com assistente de carreira IA
  - Body: `{"mensagem": "sua pergunta"}`
  - Retorna: `{"sucesso": true, "resposta": "...", "tokens_usados": 123}`

### Notificações
- `GET /api/notificacoes/` - Listar notificações do usuário
- `POST /api/notificacoes/<id>/ler/` - Marcar como lida

### Mensagens
- `POST /api/mensagens/enviar/` - Enviar mensagem
  - Body: `{"destinatario_id": 1, "assunto": "...", "conteudo": "..."}`
- `POST /api/mensagens/<id>/marcar-lida/` - Marcar como lida

## Configuração e Variáveis de Ambiente

### Variáveis Obrigatórias
- `DATABASE_URL` - URL de conexão PostgreSQL (configurado automaticamente)
- `OPENAI_API_KEY` - Chave da API OpenAI para chat IA

### Configurações do Django
- `DEBUG = True` (desenvolvimento)
- `ALLOWED_HOSTS = ['*']` (para proxy do Replit)
- `CSRF_TRUSTED_ORIGINS` - Domínios Replit permitidos
- `LANGUAGE_CODE = 'pt-br'`
- `TIME_ZONE = 'America/Sao_Paulo'`

## Como Executar

### Desenvolvimento
O servidor inicia automaticamente via workflow:
```bash
python manage.py runserver 0.0.0.0:5000
```

### Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### Criar Superusuário
```bash
python manage.py createsuperuser
```

### Admin Panel
Acesse `/gerenciador/` para o painel administrativo do Django

## Dependências
```
django>=5.2.8
gunicorn>=23.0.0
psycopg2-binary>=2.9.10
dj-database-url>=2.3.0
openai>=1.58.1
```

## Histórico de Mudanças Recentes

### 2025-11-19: Sistema Completo e Robusto - Versão Final
- ✅ **PostgreSQL**: Migração para banco de dados PostgreSQL em produção
- ✅ **Modelo Candidatura**: Sistema completo de candidaturas com status, cartas e observações
- ✅ **Matching Configurável**: Pesos parametrizados em settings com validação robusta
- ✅ **Algoritmo Null-Safe**: Proteção contra dados vazios em localização e salário
- ✅ **APIs Validadas**: Validação completa de inputs, permissões e tratamento de erros
- ✅ **Signals Robustos**: Guards contra crashes em notificações automáticas
- ✅ **Sistema de Notificações**: Alertas inteligentes para matches, candidaturas e mensagens
- ✅ **Dados de Exemplo**: Comando `criar_dados_exemplo` para popular banco com dados realistas
- ✅ **Autenticação Completa**: Login/cadastro com validação e redirecionamento inteligente
- ✅ **Dashboards Otimizados**: Queries eficientes com select_related/prefetch
- ✅ **Chat IA**: Assistente virtual com OpenAI GPT-4o-mini
- ✅ **Área Administrativa**: Painel completo para gerenciar plataforma

### 2025-11-18: Setup Inicial e Algoritmo de Matching
- Configuração inicial do ambiente Replit
- Implementação do algoritmo de matching
- Criação de 7 modelos principais
- APIs RESTful para matching

## Próximos Passos Sugeridos
1. 🎨 **UI/UX**: Melhorar design e responsividade dos templates
2. 📧 **Email**: Sistema de emails para recuperação de senha
3. 📊 **Analytics**: Dashboard com gráficos e estatísticas avançadas
4. 🔍 **Busca Avançada**: Elasticsearch ou busca full-text
5. 📱 **PWA**: Transformar em Progressive Web App
6. 🤖 **ML**: Melhorar matching com machine learning
7. 📄 **PDF**: Geração de currículos em PDF
8. 🔔 **Push Notifications**: Notificações em tempo real via WebSockets

## Notas de Desenvolvimento

### Segurança
- Todas as senhas são hasheadas com PBKDF2
- CSRF protection ativo em todos os formulários
- XSS protection via templates Django
- SQL injection prevenido via ORM
- Validação de permissões em todas as APIs (role-based access control)

### Robustez
- Algoritmo de matching null-safe para dados vazios
- Pesos de matching validados automaticamente
- Signals com guards para evitar crashes
- APIs com validação completa de inputs
- Tratamento de erros com códigos HTTP apropriados (400, 403, 404, 500)

### Performance
- Queries otimizadas com select_related/prefetch_related
- Cache de contadores em dashboards
- Índices de banco de dados em campos críticos
- Matches gerados automaticamente ao criar vagas

### IA
- Chat usa modelo GPT-4o-mini (econômico e eficiente)
- Sistema de tokens controlado
- Prompts otimizados para carreira profissional

## Autor e Manutenção
Projeto desenvolvido para conectar talentos com oportunidades de forma inteligente e eficiente.
