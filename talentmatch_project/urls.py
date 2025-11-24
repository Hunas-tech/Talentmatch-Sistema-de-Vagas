 # CAMINHO: PROJETOTCC/talentmatch_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL para o admin padrão do Django (alterada para não haver conflito)
    path('gerenciador/', admin.site.urls),

    # CORREÇÃO DEFINITIVA: 
    # Esta linha direciona TODAS as outras URLs (incluindo '/perfil/') 
    # para serem tratadas pelo ficheiro urls.py do nosso app 'core'.
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


