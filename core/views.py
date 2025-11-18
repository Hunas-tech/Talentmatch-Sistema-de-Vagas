from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Candidato, Empresa, Vaga, Match, Curso, ProgressoCurso
from .matching import gerar_matches_para_candidato, gerar_matches_para_vaga, calcular_compatibilidade
from datetime import datetime


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
    vagas = Vaga.objects.filter(status='aberta').order_by('-criado_em')
    return render(request, 'explorar_vagas.html', {'vagas': vagas})

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
    """Página de cadastro da empresa."""
    if request.method == "POST":
        # Criar a empresa no banco de dados
        empresa = Empresa.objects.create(
            nome=request.POST.get('nome', ''),
            cnpj=request.POST.get('cnpj', ''),
            email=request.POST.get('email', ''),
            telefone=request.POST.get('telefone', ''),
            endereco=request.POST.get('endereco', ''),
            cidade=request.POST.get('cidade', ''),
            estado=request.POST.get('estado', ''),
            setor=request.POST.get('setor', ''),
            descricao=request.POST.get('descricao', ''),
        )
        
        # Salvar ID da empresa na sessão
        request.session['empresa_id'] = empresa.id
        
        # Redireciona para o dashboard da empresa após cadastro
        return redirect("dashboard_empresa")
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
    if request.method == "POST":
        # Processar o login aqui (por enquanto apenas simula)
        email = request.POST.get('email')
        print(f"LOGIN - Email: {email}")
        # Por padrão, redireciona para dashboard do candidato
        # Em uma implementação real, verificaria o tipo de usuário
        return redirect("dashboard_candidato")
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
    if request.method == "POST":
        # Criar o candidato no banco de dados
        candidato = Candidato.objects.create(
            nome=request.POST.get('nome', ''),
            email=request.POST.get('email', ''),
            telefone=request.POST.get('telefone', ''),
            data_nascimento=request.POST.get('nascimento') or None,
            sexo=request.POST.get('sexo', ''),
            pronomes=request.POST.get('pronomes', ''),
            cidade=request.POST.get('cidade', ''),
            estado=request.POST.get('estado', ''),
            pcd=request.POST.get('pcd') == 'on',
        )
        
        # Salvar ID do candidato na sessão
        request.session['candidato_id'] = candidato.id
        
        # Redireciona para o dashboard do candidato após cadastro
        return redirect("dashboard_candidato")
    return render(request, 'cadastro.html')

def sair(request):
    logout(request)
    return redirect('landing_page')


# ===============================
# 🎯 API DE MATCHING
# ===============================

@require_http_methods(["GET"])
def api_gerar_matches_candidato(request, candidato_id):
    """
    API: Gera matches para um candidato específico
    GET /api/matches/candidato/<id>/
    """
    try:
        candidato = Candidato.objects.get(id=candidato_id)
        matches = gerar_matches_para_candidato(candidato_id, score_minimo=40)
        
        data = {
            'candidato': {
                'id': candidato.id,
                'nome': candidato.nome,
                'email': candidato.email
            },
            'total_matches': len(matches),
            'matches': [
                {
                    'id': match.id,
                    'vaga': {
                        'id': match.vaga.id,
                        'titulo': match.vaga.titulo,
                        'empresa': match.vaga.empresa.nome,
                        'cidade': match.vaga.cidade,
                        'tipo': match.vaga.tipo,
                        'nivel': match.vaga.nivel,
                    },
                    'score': match.score,
                    'status': match.status,
                }
                for match in matches[:10]  # Top 10 matches
            ]
        }
        return JsonResponse(data)
    except Candidato.DoesNotExist:
        return JsonResponse({'error': 'Candidato não encontrado'}, status=404)


@require_http_methods(["GET"])
def api_gerar_matches_vaga(request, vaga_id):
    """
    API: Gera matches para uma vaga específica
    GET /api/matches/vaga/<id>/
    """
    try:
        vaga = Vaga.objects.get(id=vaga_id)
        matches = gerar_matches_para_vaga(vaga_id, score_minimo=40)
        
        data = {
            'vaga': {
                'id': vaga.id,
                'titulo': vaga.titulo,
                'empresa': vaga.empresa.nome,
            },
            'total_matches': len(matches),
            'matches': [
                {
                    'id': match.id,
                    'candidato': {
                        'id': match.candidato.id,
                        'nome': match.candidato.nome,
                        'cidade': match.candidato.cidade,
                        'experiencia_anos': match.candidato.experiencia_anos,
                    },
                    'score': match.score,
                    'status': match.status,
                }
                for match in matches[:10]  # Top 10 matches
            ]
        }
        return JsonResponse(data)
    except Vaga.DoesNotExist:
        return JsonResponse({'error': 'Vaga não encontrada'}, status=404)


@require_http_methods(["POST"])
def api_aplicar_vaga(request, vaga_id):
    """
    API: Candidato aplica para uma vaga
    POST /api/vaga/<id>/aplicar/
    """
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return JsonResponse({'error': 'Candidato não autenticado'}, status=401)
    
    try:
        candidato = Candidato.objects.get(id=candidato_id)
        vaga = Vaga.objects.get(id=vaga_id)
        
        # Verifica se já existe match
        match, created = Match.objects.get_or_create(
            candidato=candidato,
            vaga=vaga,
            defaults={
                'score': calcular_compatibilidade(candidato, vaga),
                'candidato_interessado': True
            }
        )
        
        if not created:
            # Se já existe, atualiza o interesse
            match.candidato_interessado = True
            match.save()
        
        return JsonResponse({
            'success': True,
            'match_id': match.id,
            'score': match.score,
            'created': created
        })
    except (Candidato.DoesNotExist, Vaga.DoesNotExist) as e:
        return JsonResponse({'error': str(e)}, status=404)


@require_http_methods(["GET"])
def api_meus_matches(request):
    """
    API: Retorna matches do candidato logado
    GET /api/meus-matches/
    """
    candidato_id = request.session.get('candidato_id')
    if not candidato_id:
        return JsonResponse({'error': 'Candidato não autenticado'}, status=401)
    
    matches = Match.objects.filter(
        candidato_id=candidato_id
    ).select_related('vaga', 'vaga__empresa').order_by('-score')
    
    data = {
        'total': matches.count(),
        'matches': [
            {
                'id': match.id,
                'vaga': {
                    'id': match.vaga.id,
                    'titulo': match.vaga.titulo,
                    'empresa': match.vaga.empresa.nome,
                    'cidade': match.vaga.cidade,
                    'tipo': match.vaga.tipo,
                },
                'score': match.score,
                'status': match.status,
                'candidato_interessado': match.candidato_interessado,
            }
            for match in matches[:20]
        ]
    }
    return JsonResponse(data)