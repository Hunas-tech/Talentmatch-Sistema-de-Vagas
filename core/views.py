from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Candidato, Empresa, Vaga, Match, Candidatura, Curso, ProgressoCurso, Notificacao, Mensagem
from .matching import gerar_matches_para_candidato, gerar_matches_para_vaga, calcular_compatibilidade
from .forms import CandidatoPerfilForm, EmpresaPerfilForm
from datetime import datetime
import os
import json
from openai import OpenAI


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
    """Página de perfil do candidato (visualização)."""
    try:
        candidato = request.user.candidato
    except:
        messages.error(request, 'Perfil não encontrado.')
        return redirect('dashboard_candidato')
    
    return render(request, 'perfil_candidato.html', {'candidato': candidato})


@login_required(login_url='login')
def editar_perfil_candidato(request):
    """Edição completa de perfil do candidato com formulário estruturado."""
    try:
        candidato = request.user.candidato
    except:
        messages.error(request, 'Perfil de candidato não encontrado.')
        return redirect('dashboard_candidato')
    
    if request.method == "POST":
        form = CandidatoPerfilForm(request.POST, instance=candidato, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('dashboard_candidato')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = CandidatoPerfilForm(instance=candidato, user=request.user)
    
    context = {
        'form': form,
        'candidato': candidato,
    }
    return render(request, 'editar_perfil_candidato.html', context)

def analise(request):
    """Página de análise de perfil do candidato."""
    return render(request, 'analise.html')


# ----- 📬 Mensagens e Chat -----

@login_required(login_url='login')
def caixa_mensagens(request):
    """Caixa de mensagens funcional."""
    mensagens_recebidas = Mensagem.objects.filter(
        destinatario=request.user
    ).select_related('remetente').order_by('-criado_em')
    
    mensagens_enviadas = Mensagem.objects.filter(
        remetente=request.user
    ).select_related('destinatario').order_by('-criado_em')
    
    context = {
        'mensagens_recebidas': mensagens_recebidas[:20],
        'mensagens_enviadas': mensagens_enviadas[:20],
        'nao_lidas': mensagens_recebidas.filter(lida=False).count(),
    }
    return render(request, 'mensagens.html', context)

@login_required(login_url='login')
def chat_ia(request):
    """Chat com IA usando OpenAI."""
    try:
        candidato = request.user.candidato
        context = {'candidato': candidato}
        return render(request, 'chat_ia.html', context)
    except:
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

@login_required(login_url='login')
def cursos(request):
    """Lista de cursos disponíveis com recomendações."""
    try:
        candidato = request.user.candidato
        cursos_disponiveis = Curso.objects.all().order_by('-criado_em')
        cursos_em_andamento = ProgressoCurso.objects.filter(
            candidato=candidato,
            concluido=False
        ).select_related('curso')
        
        context = {
            'cursos': cursos_disponiveis,
            'cursos_em_andamento': cursos_em_andamento,
            'candidato': candidato,
        }
        return render(request, 'cursos.html', context)
    except:
        cursos_disponiveis = Curso.objects.all().order_by('-criado_em')
        return render(request, 'cursos.html', {'cursos': cursos_disponiveis})

@login_required(login_url='login')
def progre_cursos(request):
    """Progresso em cursos realizados."""
    try:
        candidato = request.user.candidato
        progressos = ProgressoCurso.objects.filter(
            candidato=candidato
        ).select_related('curso').order_by('-iniciado_em')
        
        concluidos = progressos.filter(concluido=True)
        em_andamento = progressos.filter(concluido=False)
        
        context = {
            'progressos': progressos,
            'concluidos': concluidos,
            'em_andamento': em_andamento,
            'total_cursos': progressos.count(),
            'total_concluidos': concluidos.count(),
        }
        return render(request, 'progre_cursos.html', context)
    except:
        messages.error(request, 'Perfil de candidato não encontrado.')
        return redirect('login')


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
    mensagens_nao_lidas = Mensagem.objects.filter(destinatario=request.user, lida=False).count()
    
    context = {
        'empresa': empresa,
        'vagas': vagas[:10],
        'vagas_abertas_count': vagas_abertas.count(),
        'total_vagas': vagas.count(),
        'total_candidatos': total_candidatos,
        'mensagens_nao_lidas': mensagens_nao_lidas,
    }
    return render(request, 'dashboard_empresa.html', context)


@login_required(login_url='login')
def editar_perfil_empresa(request):
    """Edição completa de perfil da empresa com formulário estruturado."""
    try:
        empresa = request.user.empresa
    except:
        messages.error(request, 'Perfil de empresa não encontrado.')
        return redirect('dashboard_empresa')
    
    if request.method == "POST":
        form = EmpresaPerfilForm(request.POST, instance=empresa, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil da empresa atualizado com sucesso!')
            return redirect('dashboard_empresa')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = EmpresaPerfilForm(instance=empresa, user=request.user)
    
    context = {
        'form': form,
        'empresa': empresa,
    }
    return render(request, 'editar_perfil_empresa.html', context)


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

@login_required(login_url='login')
def dashboard_admin(request):
    """Painel principal do administrador com estatísticas."""
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('landing')
    
    total_candidatos = Candidato.objects.count()
    total_empresas = Empresa.objects.count()
    total_vagas = Vaga.objects.count()
    vagas_abertas = Vaga.objects.filter(status='aberta').count()
    total_matches = Match.objects.count()
    matches_ativos = Match.objects.filter(status='pendente').count()
    
    candidatos_recentes = Candidato.objects.order_by('-criado_em')[:5]
    empresas_recentes = Empresa.objects.order_by('-criado_em')[:5]
    vagas_recentes = Vaga.objects.select_related('empresa').order_by('-criado_em')[:5]
    
    context = {
        'total_candidatos': total_candidatos,
        'total_empresas': total_empresas,
        'total_vagas': total_vagas,
        'vagas_abertas': vagas_abertas,
        'total_matches': total_matches,
        'matches_ativos': matches_ativos,
        'candidatos_recentes': candidatos_recentes,
        'empresas_recentes': empresas_recentes,
        'vagas_recentes': vagas_recentes,
    }
    return render(request, 'dashboard_admin.html', context)

@login_required(login_url='login')
def gerenciar_usuarios(request):
    """Página de gerenciamento de usuários (candidatos) com filtros."""
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('landing')
    
    candidatos = Candidato.objects.all().select_related('user').order_by('-criado_em')
    
    busca = request.GET.get('busca', '')
    if busca:
        candidatos = candidatos.filter(nome__icontains=busca) | candidatos.filter(email__icontains=busca)
    
    context = {
        'candidatos': candidatos[:100],
        'total': candidatos.count(),
        'busca': busca,
    }
    return render(request, 'gerenciar_usuarios.html', context)

@login_required(login_url='login')
def gerenciar_empresas(request):
    """Página de gerenciamento de empresas com filtros."""
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('landing')
    
    empresas = Empresa.objects.all().select_related('user').order_by('-criado_em')
    
    busca = request.GET.get('busca', '')
    if busca:
        empresas = empresas.filter(nome__icontains=busca) | empresas.filter(cnpj__icontains=busca)
    
    context = {
        'empresas': empresas[:100],
        'total': empresas.count(),
        'busca': busca,
    }
    return render(request, 'gerenciar_empresas.html', context)

@login_required(login_url='login')
def gerenciar_vagas(request):
    """Página de gerenciamento de vagas com filtros."""
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('landing')
    
    vagas = Vaga.objects.all().select_related('empresa').order_by('-criado_em')
    
    status_filtro = request.GET.get('status', '')
    if status_filtro:
        vagas = vagas.filter(status=status_filtro)
    
    context = {
        'vagas': vagas[:100],
        'total': vagas.count(),
        'status_filtro': status_filtro,
    }
    return render(request, 'gerenciar_vagas.html', context)

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


# ===============================
# 🤖 API DO CHAT COM IA
# ===============================

@require_http_methods(["POST"])
@login_required(login_url='login')
def api_chat_ia(request):
    """
    API: Chat com IA usando OpenAI
    POST /api/chat/ia/
    Body: {"mensagem": "texto da mensagem"}
    """
    try:
        data = json.loads(request.body)
        mensagem_usuario = data.get('mensagem', '').strip()
        
        if not mensagem_usuario:
            return JsonResponse({'error': 'Mensagem vazia'}, status=400)
        
        try:
            candidato = request.user.candidato
            perfil_contexto = f"""
Você é um assistente de carreira inteligente do TalentMatch.
Candidato: {candidato.nome}
Habilidades: {candidato.habilidades}
Experiência: {candidato.experiencia_anos} anos
Área de interesse: {candidato.area_interesse}
Escolaridade: {candidato.escolaridade}
"""
        except:
            perfil_contexto = "Você é um assistente de carreira inteligente do TalentMatch."
        
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return JsonResponse({'error': 'API key não configurada'}, status=500)
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": perfil_contexto + "\nAjude o candidato com orientação de carreira, dicas para entrevistas, sugestões de habilidades para desenvolver e análise de compatibilidade com vagas. Seja amigável, profissional e objetivo."},
                {"role": "user", "content": mensagem_usuario}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        resposta_ia = response.choices[0].message.content
        
        return JsonResponse({
            'sucesso': True,
            'resposta': resposta_ia,
            'tokens_usados': response.usage.total_tokens
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ===============================
# 🔔 API DE NOTIFICAÇÕES
# ===============================

@require_http_methods(["GET"])
@login_required(login_url='login')
def api_notificacoes(request):
    """
    API: Retorna notificações do usuário
    GET /api/notificacoes/
    """
    notificacoes = Notificacao.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')[:20]
    
    data = {
        'total': notificacoes.count(),
        'nao_lidas': notificacoes.filter(lida=False).count(),
        'notificacoes': [
            {
                'id': n.id,
                'tipo': n.tipo,
                'titulo': n.titulo,
                'mensagem': n.mensagem,
                'lida': n.lida,
                'url': n.url,
                'criado_em': n.criado_em.isoformat(),
            }
            for n in notificacoes
        ]
    }
    return JsonResponse(data)


@require_http_methods(["POST"])
@login_required(login_url='login')
def api_marcar_notificacao_lida(request, id):
    """
    API: Marca uma notificação como lida
    POST /api/notificacoes/<id>/ler/
    """
    try:
        notificacao = Notificacao.objects.get(id=id, usuario=request.user)
        notificacao.lida = True
        notificacao.save()
        return JsonResponse({'sucesso': True})
    except Notificacao.DoesNotExist:
        return JsonResponse({'error': 'Notificação não encontrada'}, status=404)


# ===============================
# 💬 API DE MENSAGENS
# ===============================

@require_http_methods(["POST"])
@login_required(login_url='login')
def api_enviar_mensagem(request):
    """
    API: Envia uma mensagem
    POST /api/mensagens/enviar/
    Body: {"destinatario_id": 1, "assunto": "...", "conteudo": "..."}
    """
    try:
        data = json.loads(request.body)
        destinatario_id = data.get('destinatario_id')
        assunto = data.get('assunto', '').strip()
        conteudo = data.get('conteudo', '').strip()
        
        if not all([destinatario_id, assunto, conteudo]):
            return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)
        
        destinatario = User.objects.get(id=destinatario_id)
        
        mensagem = Mensagem.objects.create(
            remetente=request.user,
            destinatario=destinatario,
            assunto=assunto,
            conteudo=conteudo
        )
        
        Notificacao.objects.create(
            usuario=destinatario,
            tipo='mensagem',
            titulo='Nova mensagem',
            mensagem=f'{request.user.first_name} enviou uma mensagem: {assunto}',
            url='/mensagens/'
        )
        
        return JsonResponse({
            'sucesso': True,
            'mensagem_id': mensagem.id
        })
        
    except User.DoesNotExist:
        return JsonResponse({'error': 'Destinatário não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required(login_url='login')
def api_marcar_mensagem_lida(request, id):
    """
    API: Marca uma mensagem como lida
    POST /api/mensagens/<id>/marcar-lida/
    """
    try:
        mensagem = Mensagem.objects.get(id=id, destinatario=request.user)
        mensagem.lida = True
        mensagem.save()
        return JsonResponse({'sucesso': True})
    except Mensagem.DoesNotExist:
        return JsonResponse({'error': 'Mensagem não encontrada'}, status=404)


@require_http_methods(["POST"])
@login_required(login_url='login')
def api_candidatar_vaga(request, vaga_id):
    """
    API: Candidata-se a uma vaga
    POST /api/vagas/<vaga_id>/candidatar/
    """
    try:
        candidato = request.user.candidato
    except AttributeError:
        return JsonResponse({'error': 'Você precisa ser um candidato para se candidatar'}, status=403)
    
    try:
        vaga = Vaga.objects.get(id=vaga_id, status='aberta')
    except Vaga.DoesNotExist:
        return JsonResponse({'error': 'Vaga não encontrada ou não está mais disponível'}, status=404)
    
    if Candidatura.objects.filter(candidato=candidato, vaga=vaga).exists():
        return JsonResponse({'error': 'Você já se candidatou a esta vaga'}, status=400)
    
    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    
    carta_apresentacao = data.get('carta_apresentacao', '')
    if carta_apresentacao and len(carta_apresentacao) > 2000:
        return JsonResponse({'error': 'Carta de apresentação muito longa (máximo 2000 caracteres)'}, status=400)
    
    try:
        match = Match.objects.filter(candidato=candidato, vaga=vaga).first()
        if not match:
            score = calcular_compatibilidade(candidato, vaga)
            match = Match.objects.create(candidato=candidato, vaga=vaga, score=score)
        
        candidatura = Candidatura.objects.create(
            candidato=candidato,
            vaga=vaga,
            match=match,
            carta_apresentacao=carta_apresentacao
        )
        
        messages.success(request, f'Candidatura enviada com sucesso para a vaga {vaga.titulo}!')
        return JsonResponse({
            'sucesso': True,
            'candidatura_id': candidatura.id,
            'status': candidatura.status
        })
    except Exception as e:
        return JsonResponse({'error': f'Erro ao criar candidatura: {str(e)}'}, status=500)


@require_http_methods(["POST"])
@login_required(login_url='login')
def api_atualizar_candidatura(request, candidatura_id):
    """
    API: Atualiza status de uma candidatura (empresa)
    POST /api/candidaturas/<candidatura_id>/atualizar/
    """
    try:
        empresa = request.user.empresa
    except AttributeError:
        return JsonResponse({'error': 'Acesso negado: você precisa ser uma empresa'}, status=403)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    
    status = data.get('status')
    if not status:
        return JsonResponse({'error': 'Status é obrigatório'}, status=400)
    
    status_validos = [choice[0] for choice in Candidatura.STATUS_CHOICES]
    if status not in status_validos:
        return JsonResponse({'error': f'Status inválido. Valores permitidos: {", ".join(status_validos)}'}, status=400)
    
    try:
        candidatura = Candidatura.objects.get(id=candidatura_id, vaga__empresa=empresa)
    except Candidatura.DoesNotExist:
        return JsonResponse({'error': 'Candidatura não encontrada ou você não tem permissão para atualizá-la'}, status=404)
    
    observacoes = data.get('observacoes', '')
    if observacoes and len(observacoes) > 1000:
        return JsonResponse({'error': 'Observações muito longas (máximo 1000 caracteres)'}, status=400)
    
    try:
        candidatura.status = status
        if observacoes:
            candidatura.observacoes_empresa = observacoes
        candidatura.save()
        
        return JsonResponse({
            'sucesso': True,
            'status': candidatura.status,
            'mensagem': 'Candidatura atualizada com sucesso'
        })
    except Exception as e:
        return JsonResponse({'error': f'Erro ao atualizar candidatura: {str(e)}'}, status=500)


@login_required(login_url='login')
def listar_candidaturas_candidato(request):
    """Lista todas as candidaturas do candidato"""
    try:
        candidato = request.user.candidato
        candidaturas = Candidatura.objects.filter(
            candidato=candidato
        ).select_related('vaga', 'vaga__empresa', 'match').order_by('-criado_em')
        
        context = {
            'candidaturas': candidaturas,
        }
        return render(request, 'candidaturas_vagas.html', context)
    except:
        messages.error(request, 'Perfil de candidato não encontrado.')
        return redirect('home')


@login_required(login_url='login')
def listar_candidaturas_empresa(request):
    """Lista todas as candidaturas para vagas da empresa"""
    try:
        empresa = request.user.empresa
        candidaturas = Candidatura.objects.filter(
            vaga__empresa=empresa
        ).select_related('candidato', 'vaga', 'match').order_by('-criado_em')
        
        context = {
            'candidaturas': candidaturas,
        }
        return render(request, 'gerenciar_candidaturas.html', context)
    except:
        messages.error(request, 'Perfil de empresa não encontrado.')
        return redirect('home')