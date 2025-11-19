from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from .models import Candidato, Empresa, Vaga, Match, Curso, ProgressoCurso
from .matching import gerar_matches_para_candidato, gerar_matches_para_vaga, calcular_compatibilidade
from datetime import datetime


# ===============================
# 🛠️ FUNÇÕES AUXILIARES
# ===============================

def _redirect_authenticated_user(user):
    """Redireciona usuário autenticado para o dashboard apropriado."""
    if user.is_superuser or user.is_staff:
        return redirect('dashboard_admin')
    
    try:
        if hasattr(user, 'candidato'):
            return redirect('dashboard_candidato')
        elif hasattr(user, 'empresa'):
            return redirect('dashboard_empresa')
    except:
        pass
    
    return redirect('dashboard_candidato')


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

@login_required(login_url='login')
def dashboard_candidato(request):
    """Dashboard principal do candidato."""
    try:
        candidato = request.user.candidato
    except:
        messages.error(request, 'Perfil de candidato não encontrado.')
        return redirect('login')
    
    matches = Match.objects.filter(candidato=candidato).select_related('vaga', 'vaga__empresa').order_by('-score')[:5]
    vagas_recentes = Vaga.objects.filter(status='aberta').order_by('-criado_em')[:10]
    
    context = {
        'candidato': candidato,
        'matches': matches,
        'vagas_recentes': vagas_recentes,
    }
    return render(request, 'dashboard_candidato.html', context)

@login_required(login_url='login')
def perfil_candidato(request):
    """Página de perfil do candidato."""
    try:
        candidato = request.user.candidato
    except:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('dashboard_candidato')
    
    if request.method == "POST":
        candidato.nome = request.POST.get('nome', candidato.nome)
        candidato.telefone = request.POST.get('telefone', candidato.telefone)
        candidato.cidade = request.POST.get('cidade', candidato.cidade)
        candidato.estado = request.POST.get('estado', candidato.estado)
        candidato.habilidades = request.POST.get('habilidades', candidato.habilidades)
        candidato.experiencia_anos = int(request.POST.get('experiencia_anos', 0) or 0)
        candidato.escolaridade = request.POST.get('escolaridade', candidato.escolaridade)
        candidato.area_interesse = request.POST.get('area_interesse', candidato.area_interesse)
        
        pretensao = request.POST.get('pretensao_salarial', '')
        if pretensao:
            try:
                candidato.pretensao_salarial = float(pretensao)
            except ValueError:
                pass
        
        candidato.curriculo = request.POST.get('curriculo', candidato.curriculo)
        candidato.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('perfil_candidato')
    
    return render(request, 'perfil_candidato.html', {'candidato': candidato})

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

@login_required(login_url='login')
def explorar_vagas(request):
    """Página de exploração de vagas com filtragem."""
    vagas = Vaga.objects.filter(status='aberta').select_related('empresa').order_by('-criado_em')
    
    cidade = request.GET.get('cidade', '')
    tipo = request.GET.get('tipo', '')
    nivel = request.GET.get('nivel', '')
    
    if cidade:
        vagas = vagas.filter(cidade__icontains=cidade)
    if tipo:
        vagas = vagas.filter(tipo=tipo)
    if nivel:
        vagas = vagas.filter(nivel=nivel)
    
    context = {
        'vagas': vagas[:50],
        'total': vagas.count(),
        'filtros': {
            'cidade': cidade,
            'tipo': tipo,
            'nivel': nivel,
        }
    }
    return render(request, 'explorar_vagas.html', context)

@login_required(login_url='login')
def candidaturas_vagas(request):
    """Página que lista candidaturas/matches do candidato."""
    try:
        candidato = request.user.candidato
        matches = Match.objects.filter(
            candidato=candidato,
            candidato_interessado=True
        ).select_related('vaga', 'vaga__empresa').order_by('-criado_em')
        
        context = {
            'matches': matches,
            'total': matches.count(),
        }
        return render(request, 'candidaturas_vagas.html', context)
    except:
        messages.error(request, 'Perfil de candidato não encontrado.')
        return redirect('login')

@login_required(login_url='login')
def detalhe_vaga(request, id):
    """Detalhes de uma vaga com opção de candidatura."""
    vaga = get_object_or_404(Vaga, id=id)
    
    try:
        candidato = request.user.candidato
        match = Match.objects.filter(candidato=candidato, vaga=vaga).first()
        
        if not match:
            score = calcular_compatibilidade(candidato, vaga)
            match = Match(candidato=candidato, vaga=vaga, score=score)
        
        context = {
            'vaga': vaga,
            'match': match,
            'compatibilidade': match.score if match else 0,
        }
        return render(request, 'detalhe_vaga.html', context)
    except:
        return render(request, 'detalhe_vaga.html', {'vaga': vaga})


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

@login_required(login_url='login')
def dashboard_empresa(request):
    """Dashboard funcional da empresa."""
    try:
        empresa = request.user.empresa
    except:
        messages.error(request, 'Perfil de empresa não encontrado.')
        return redirect('login')
    
    vagas = Vaga.objects.filter(empresa=empresa).order_by('-criado_em')
    vagas_abertas = vagas.filter(status='aberta')
    total_candidatos = Match.objects.filter(vaga__empresa=empresa).count()
    
    context = {
        'empresa': empresa,
        'vagas': vagas[:10],
        'vagas_abertas_count': vagas_abertas.count(),
        'total_vagas': vagas.count(),
        'total_candidatos': total_candidatos,
    }
    return render(request, 'dashboard_empresa.html', context)

def cadastro_empresa(request):
    """Página de cadastro funcional da empresa."""
    if request.user.is_authenticated:
        return redirect('dashboard_empresa')
    
    if request.method == "POST":
        nome = request.POST.get('nome', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not all([nome, cnpj, email, password]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'cadastro_empresa.html')
        
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro_empresa.html')
        
        if len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'cadastro_empresa.html')
        
        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este email já está cadastrado.')
                return render(request, 'cadastro_empresa.html')
            
            if Empresa.objects.filter(cnpj=cnpj).exists():
                messages.error(request, 'Este CNPJ já está cadastrado.')
                return render(request, 'cadastro_empresa.html')
            
            username = 'empresa_' + email.split('@')[0] + str(User.objects.count() + 1)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nome
            )
            
            empresa = Empresa.objects.create(
                user=user,
                nome=nome,
                cnpj=cnpj,
                email=email,
                telefone=request.POST.get('telefone', ''),
                endereco=request.POST.get('endereco', ''),
                cidade=request.POST.get('cidade', ''),
                estado=request.POST.get('estado', ''),
                setor=request.POST.get('setor', ''),
                descricao=request.POST.get('descricao', ''),
            )
            
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo ao TalentMatch!')
            return redirect("dashboard_empresa")
            
        except IntegrityError:
            messages.error(request, 'Erro ao criar conta. Verifique os dados e tente novamente.')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
    return render(request, "cadastro_empresa.html")

@login_required(login_url='login')
def cadastrar_vaga(request):
    """Formulário funcional para cadastrar uma nova vaga."""
    try:
        empresa = request.user.empresa
    except:
        messages.error(request, 'Apenas empresas podem cadastrar vagas.')
        return redirect('login')
    
    if request.method == "POST":
        try:
            vaga = Vaga.objects.create(
                empresa=empresa,
                titulo=request.POST.get('titulo', '').strip(),
                descricao=request.POST.get('descricao', '').strip(),
                requisitos=request.POST.get('requisitos', '').strip(),
                habilidades_necessarias=request.POST.get('habilidades_necessarias', '').strip(),
                nivel=request.POST.get('nivel', 'junior'),
                tipo=request.POST.get('tipo', 'presencial'),
                cidade=request.POST.get('cidade', '').strip(),
                estado=request.POST.get('estado', '').strip(),
                salario_min=float(request.POST.get('salario_min', 0) or 0),
                salario_max=float(request.POST.get('salario_max', 0) or 0),
                experiencia_minima=int(request.POST.get('experiencia_minima', 0) or 0),
                status='aberta'
            )
            
            gerar_matches_para_vaga(vaga.id, score_minimo=40)
            
            messages.success(request, f'Vaga "{vaga.titulo}" cadastrada com sucesso!')
            return redirect('dashboard_empresa')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar vaga: {str(e)}')
    
    return render(request, 'cadastrar_vaga.html', {'empresa': empresa})


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
    """Página de login funcional."""
    if request.user.is_authenticated:
        return _redirect_authenticated_user(request.user)
    
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not email or not password:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'login.html')
        
        try:
            user = User.objects.get(email=email)
            user_auth = authenticate(request, username=user.username, password=password)
            
            if user_auth is not None:
                login(request, user_auth)
                messages.success(request, f'Bem-vindo(a) de volta!')
                return _redirect_authenticated_user(user_auth)
            else:
                messages.error(request, 'Senha incorreta.')
        except User.DoesNotExist:
            messages.error(request, 'Email não encontrado.')
    
    return render(request, 'login.html')

def logout_view(request):
    """Efetua logout e redireciona para a landing page."""
    logout(request)
    messages.success(request, 'Você saiu da sua conta com sucesso!')
    return redirect("landing")


# ===============================
# 📝 CADASTRO GERAL (CANDIDATO)
# ===============================

def cadastro(request):
    """Página de cadastro funcional do candidato."""
    if request.user.is_authenticated:
        return redirect('dashboard_candidato')
    
    if request.method == "POST":
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not all([nome, email, password]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'cadastro.html')
        
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')
        
        if len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'cadastro.html')
        
        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este email já está cadastrado.')
                return render(request, 'cadastro.html')
            
            username = email.split('@')[0] + str(User.objects.count() + 1)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nome
            )
            
            candidato = Candidato.objects.create(
                user=user,
                nome=nome,
                email=email,
                telefone=request.POST.get('telefone', ''),
                data_nascimento=request.POST.get('nascimento') or None,
                sexo=request.POST.get('sexo', ''),
                pronomes=request.POST.get('pronomes', ''),
                cidade=request.POST.get('cidade', ''),
                estado=request.POST.get('estado', ''),
                pcd=request.POST.get('pcd') == 'on',
            )
            
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo ao TalentMatch!')
            return redirect("dashboard_candidato")
            
        except IntegrityError:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
        except Exception as e:
            messages.error(request, f'Erro inesperado: {str(e)}')
    
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