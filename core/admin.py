from django.contrib import admin
from .models import Candidato, Empresa, Vaga, Match, Mensagem, Curso, ProgressoCurso


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'cidade', 'estado', 'experiencia_anos', 'criado_em']
    list_filter = ['estado', 'pcd', 'criado_em']
    search_fields = ['nome', 'email', 'habilidades']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'email', 'cidade', 'estado', 'setor', 'criado_em']
    list_filter = ['estado', 'setor', 'criado_em']
    search_fields = ['nome', 'cnpj', 'email']


@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'nivel', 'tipo', 'cidade', 'estado', 'status', 'criado_em']
    list_filter = ['nivel', 'tipo', 'status', 'estado', 'criado_em']
    search_fields = ['titulo', 'descricao', 'empresa__nome']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['candidato', 'vaga', 'score', 'status', 'candidato_interessado', 'empresa_interessada', 'criado_em']
    list_filter = ['status', 'score', 'criado_em']
    search_fields = ['candidato__nome', 'vaga__titulo']
    ordering = ['-score', '-criado_em']


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ['remetente', 'destinatario', 'assunto', 'lida', 'criado_em']
    list_filter = ['lida', 'criado_em']
    search_fields = ['assunto', 'conteudo', 'remetente__username', 'destinatario__username']


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'nivel', 'duracao_horas', 'criado_em']
    list_filter = ['categoria', 'nivel', 'criado_em']
    search_fields = ['titulo', 'descricao']


@admin.register(ProgressoCurso)
class ProgressoCursoAdmin(admin.ModelAdmin):
    list_display = ['candidato', 'curso', 'progresso', 'concluido', 'iniciado_em']
    list_filter = ['concluido', 'iniciado_em']
    search_fields = ['candidato__nome', 'curso__titulo']
