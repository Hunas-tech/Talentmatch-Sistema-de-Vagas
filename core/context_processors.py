def user_type(request):
    """
    Context processor que adiciona informações sobre o tipo de usuário
    ao contexto de todos os templates, verificando apenas uma vez por request.
    
    Usa queries diretas ao banco de dados para evitar invocar descriptors
    que lançam exceções quando o relacionamento não existe.
    """
    context = {
        'is_empresa': False,
        'is_candidato': False,
        'is_staff_only': False,
        'user_empresa': None,
        'user_candidato': None,
    }
    
    if request.user.is_authenticated:
        from core.models import Empresa, Candidato
        
        user_empresa = Empresa.objects.filter(user_id=request.user.id).first()
        if user_empresa:
            context['user_empresa'] = user_empresa
            context['is_empresa'] = True
        
        user_candidato = Candidato.objects.filter(user_id=request.user.id).first()
        if user_candidato:
            context['user_candidato'] = user_candidato
            context['is_candidato'] = True
        
        if not user_empresa and not user_candidato and request.user.is_staff:
            context['is_staff_only'] = True
    
    return context
