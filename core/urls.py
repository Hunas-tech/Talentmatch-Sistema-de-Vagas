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
    path('editar-perfil/', views.editar_perfil_candidato, name='editar_perfil_candidato'),
    path('empresa/perfil/', views.perfil_empresa, name='perfil_empresa'),
    path('empresa/editar-perfil/', views.editar_perfil_empresa, name='editar_perfil_empresa'),

    # Vagas
    path('vagas/', views.explorar_vagas, name='explorar_vagas'),
    path('candidaturas/', views.candidaturas_vagas, name='candidaturas_vagas'),
    path('detalhe_vaga/<int:id>/', views.detalhe_vaga, name='detalhe_vaga'),
    path('cadastrar_vaga/', views.cadastrar_vaga, name='cadastrar_vaga'),
    path('editar_vaga/<int:id>/', views.editar_vaga, name='editar_vaga'),
    path('deletar_vaga/<int:id>/', views.deletar_vaga, name='deletar_vaga'),

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

# Administração
    path('gerenciar_usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('gerenciar_empresas/', views.gerenciar_empresas, name='gerenciar_empresas'),
    path('gerenciar_vagas/', views.gerenciar_vagas, name='gerenciar_vagas'),
    path('admin/deletar_candidato/<int:id>/', views.admin_deletar_candidato, name='admin_deletar_candidato'),
    path('admin/deletar_empresa/<int:id>/', views.admin_deletar_empresa, name='admin_deletar_empresa'),
    path('admin/deletar_vaga/<int:id>/', views.admin_deletar_vaga, name='admin_deletar_vaga'),
    path('cancelar_candidatura/<int:id>/', views.cancelar_candidatura, name='cancelar_candidatura'),
    path('painel_denuncias/', views.painel_denuncias, name='painel_denuncias'),
    path('painel_denuncias_resolvidas/', views.painel_denuncias_resolvidas, name='painel_denuncias_resolvidas'),
    path('painel_denuncias_ignoradas/', views.painel_denuncias_ignoradas, name='painel_denuncias_ignoradas'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('config_admin/', views.config_admin, name='config_admin'),
    
# API de Matching
    path('api/matches/candidato/<int:candidato_id>/', views.api_gerar_matches_candidato, name='api_matches_candidato'),
    path('api/matches/vaga/<int:vaga_id>/', views.api_gerar_matches_vaga, name='api_matches_vaga'),
    path('api/vaga/<int:vaga_id>/aplicar/', views.api_aplicar_vaga, name='api_aplicar_vaga'),
    path('api/meus-matches/', views.api_meus_matches, name='api_meus_matches'),
    
# API do Chat IA
    path('api/chat/ia/', views.api_chat_ia, name='api_chat_ia'),
    
# API de Notificações
    path('api/notificacoes/', views.api_notificacoes, name='api_notificacoes'),
    path('api/notificacoes/<int:id>/ler/', views.api_marcar_notificacao_lida, name='api_marcar_notificacao_lida'),
    
# API de Mensagens
    path('api/mensagens/enviar/', views.api_enviar_mensagem, name='api_enviar_mensagem'),
    path('api/mensagens/<int:id>/marcar-lida/', views.api_marcar_mensagem_lida, name='api_marcar_mensagem_lida'),
    
# API de Candidaturas
    path('api/vagas/<int:vaga_id>/candidatar/', views.api_candidatar_vaga, name='api_candidatar_vaga'),
    path('api/candidaturas/<int:candidatura_id>/atualizar/', views.api_atualizar_candidatura, name='api_atualizar_candidatura'),
    path('minhas-candidaturas/', views.listar_candidaturas_candidato, name='listar_candidaturas'),
    path('empresa/candidaturas/', views.listar_candidaturas_empresa, name='listar_candidaturas_empresa'),
]
