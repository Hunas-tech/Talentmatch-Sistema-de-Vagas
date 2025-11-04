from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Página base
def base(request):
    return render(request, 'base.html')

# Landing page
def landing_page(request):
    return render(request, 'landing.html')

# Dashboards
def dashboard_candidato(request):
    return render(request, 'dashboard_candidato.html')

def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

def dashboard_empresa(request):
    return render(request, 'dashboard_empresa.html')

# Perfil
def perfil_candidato(request):
    return render(request, 'perfil_candidato.html')

# Vagas
def explorar_vagas(request):
    return render(request, 'explorar_vagas.html')

def candidaturas_vagas(request):
    return render(request, 'candidaturas_vagas.html')

def detalhe_vaga(request, id):
    return render(request, 'detalhe_vaga.html', {'vaga_id': id})

def cadastrar_vaga(request):
    return render(request, 'cadastrar_vaga.html')

# Mensagens / Chat
def caixa_mensagens(request):
    return render(request, 'mensagens.html')

def chat_ia(request):
    return render(request, 'chat_ia.html')

# Cursos
def cursos(request):
    return render(request, 'cursos.html')

def progre_cursos(request):
    return render(request, 'progre_cursos.html')

# Configurações
def conf(request):
    return render(request, 'conf.html')

# Login / Logout
def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return render(request, "sair.html")

# Cadastro
def cadastro(request):
    return render(request, 'cadastro.html')

def cadastro_empresa(request):
    return render(request, 'cadastro_empresa.html')

def analise(request):
    return render(request, 'analise.html')