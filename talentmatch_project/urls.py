 # CAMINHO: PROJETOTCC/talentmatch_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # URL para o admin padrão do Django (alterada para não haver conflito)
    path('gerenciador/', admin.site.urls),

    # CORREÇÃO DEFINITIVA: 
    # Esta linha direciona TODAS as outras URLs (incluindo '/perfil/') 
    # para serem tratadas pelo ficheiro urls.py do nosso app 'core'.
    path('', include('core.urls')),
]


