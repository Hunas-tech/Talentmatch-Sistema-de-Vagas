from django import template

register = template.Library()

@register.filter
def has_empresa(user):
    """Verifica se o usuário tem um perfil de empresa associado de forma eficiente."""
    if not user or not user.is_authenticated:
        return False
    
    from core.models import Empresa
    try:
        _ = user.empresa
        return True
    except Empresa.DoesNotExist:
        return False

@register.filter
def has_candidato(user):
    """Verifica se o usuário tem um perfil de candidato associado de forma eficiente."""
    if not user or not user.is_authenticated:
        return False
    
    from core.models import Candidato
    try:
        _ = user.candidato
        return True
    except Candidato.DoesNotExist:
        return False
