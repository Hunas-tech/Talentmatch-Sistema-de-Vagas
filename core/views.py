from django.shortcuts import render, redirect
from django.contrib.auth import logout


# ===============================
# 🌐 PÁGINAS GERAIS
# ===============================

def base(request):
    """Página base do site (estrutura HTML principal)."""
    return render(request, 'base.html')

def landing_page(request):
    """Página inicial pública (landing page)."""
    return render(request, 'landing.html')


# ===============================
# 👤 ÁREA DO CANDIDATO / USUÁRIO
# ===============================

def dashboard_candidato(request):
    """Dashboard principal do candidato."""
    return render(request, 'dashboard_candidato.html')

def perfil_candidato(request):
    """Página de perfil do candidato."""
    return render(request, 'perfil_candidato.html')

def analise(request):
    """Página de análise de perfil do candidato."""
    return render(request, 'analise.html')


# ----- 📬 Mensagens e Chat -----

def caixa_mensagens(request):
    """Caixa de mensagens do candidato."""
    return render(request, 'mensagens.html')

def chat_ia(request):
    """Chat com IA do candidato."""
    return render(request, 'chat_ia.html')


# ----- 💼 Vagas -----

def explorar_vagas(request):
    """Página de exploração de vagas disponíveis."""
    return render(request, 'explorar_vagas.html')

def candidaturas_vagas(request):
    """Página que lista candidaturas enviadas pelo candidato."""
    return render(request, 'candidaturas_vagas.html')

def detalhe_vaga(request, id):
    """Detalhes de uma vaga específica."""
    return render(request, 'detalhe_vaga.html', {'vaga_id': id})


# ----- 🎓 Cursos -----

def cursos(request):
    """Lista de cursos disponíveis."""
    return render(request, 'cursos.html')

def progre_cursos(request):
    """Progresso em cursos realizados."""
    return render(request, 'progre_cursos.html')


# ----- ⚙️ Configurações -----

def conf(request):
    """Página de configurações do candidato."""
    return render(request, 'conf.html')


# ===============================
# 🏢 ÁREA DA EMPRESA
# ===============================

def dashboard_empresa(request):
    """Dashboard da empresa (visualização de vagas e candidatos)."""
    return render(request, 'dashboard_empresa.html')

def cadastro_empresa(request):
    if request.method == "POST":
        print("FAKE REGISTER DA EMPRESA:")
        print(request.POST)
        return redirect("dashboard_empresa")  # Certifique-se que existe essa rota no urls.py

    return render(request, "cadastro_empresa.html")

def cadastrar_vaga(request):
    """Formulário para cadastrar uma nova vaga."""
    return render(request, 'cadastrar_vaga.html')


# ===============================
# 🧑‍💼 ÁREA ADMINISTRATIVA
# ===============================

def dashboard_admin(request):
    """Painel principal do administrador."""
    return render(request, 'dashboard_admin.html')

def gerenciar_usuarios(request):
    """Página de gerenciamento de usuários (candidatos)."""
    return render(request, 'gerenciar_usuarios.html')

def gerenciar_empresas(request):
    """Página de gerenciamento de empresas cadastradas."""
    return render(request, 'gerenciar_empresas.html')

def gerenciar_vagas(request):
    """Página de gerenciamento de vagas cadastradas."""
    return render(request, 'gerenciar_vagas.html')

def painel_denuncias(request):
    """Painel de denúncias pendentes."""
    return render(request, 'painel_denuncias.html') 

def painel_denuncias_resolvidas(request):
    """Painel de denúncias resolvidas."""
    return render(request, 'painel_denuncias_resolvidas.html')  

def painel_denuncias_ignoradas(request):
    """Painel de denúncias ignoradas."""
    return render(request, 'painel_denuncias_ignoradas.html')   

def relatorios(request):
    """Página de relatórios administrativos."""
    return render(request, 'relatorios.html')

def config_admin(request):
    """Página de configurações administrativas."""
    return render(request, 'config_admin.html')

# ===============================
# 🔐 AUTENTICAÇÃO (LOGIN / LOGOUT)
# ===============================

def login_view(request):
    """Página de login."""
    return render(request, 'login.html')

def logout_view(request):
    """Efetua logout e redireciona para a tela de login."""
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "sair.html")


# ===============================
# 📝 CADASTRO GERAL (CANDIDATO)
# ===============================

def cadastro(request):
    """Página de cadastro do candidato."""
    return render(request, 'cadastro.html')

def sair(request):
    logout(request)
    return redirect('landing_page')