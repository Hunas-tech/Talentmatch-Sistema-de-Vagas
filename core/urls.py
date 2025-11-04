from django.urls import path
from . import views

urlpatterns = [
    # Página inicial / Landing
    path('', views.landing_page, name='home'),  # root aponta para landing
    path('landing/', views.landing_page, name='landing'),

    # Dashboards
    path('base/', views.base, name='base'),
    path('dashboard_candidato/', views.dashboard_candidato, name='dashboard_candidato'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_empresa/', views.dashboard_empresa, name='dashboard_empresa'),

    # Perfil
    path('perfil/', views.perfil_candidato, name='perfil_candidato'),

    # Vagas
    path('vagas/', views.explorar_vagas, name='explorar_vagas'),
    path('candidaturas/', views.candidaturas_vagas, name='candidaturas_vagas'),
    path('detalhe_vaga/<int:id>/', views.detalhe_vaga, name='detalhe_vaga'),
    path('cadastrar_vaga/', views.cadastrar_vaga, name='cadastrar_vaga'),

    # Mensagens / Chat
    path('mensagens/', views.caixa_mensagens, name='caixa_mensagens'),
    path('chat_ia/', views.chat_ia, name='chat_ia'),

    # Cursos
    path('cursos/', views.cursos, name='cursos'),
    path('progre_cursos/', views.progre_cursos, name='progre_cursos'),

    # Configurações
    path('config/', views.conf, name='conf'),

    # Login / Logout
    path('login/', views.login_view, name='login'),
    path('sair/', views.logout_view, name='logout'),

# Cadastro
    path('cadastro/', views.cadastro, name='cadastro_candidato'),
    path('cadastro_empresa/', views.cadastro_empresa, name='cadastro_empresa'),
    path('analise/', views.analise, name='analise'),
]
