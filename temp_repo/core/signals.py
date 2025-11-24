from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match, Candidatura, Mensagem, Notificacao


@receiver(post_save, sender=Match)
def criar_notificacao_match(sender, instance, created, **kwargs):
    """Cria notificação quando um novo match é criado"""
    if not created or instance.score < 60:
        return
    
    try:
        if instance.candidato.user:
            Notificacao.objects.create(
                usuario=instance.candidato.user,
                tipo='match',
                titulo='Novo Match Encontrado!',
                mensagem=f'Você tem {instance.score}% de compatibilidade com a vaga "{instance.vaga.titulo}" da empresa {instance.vaga.empresa.nome}',
                url=f'/detalhe_vaga/{instance.vaga.id}/'
            )
    except Exception:
        pass
    
    try:
        if instance.vaga.empresa.user:
            Notificacao.objects.create(
                usuario=instance.vaga.empresa.user,
                tipo='match',
                titulo='Novo Candidato Compatível!',
                mensagem=f'O candidato {instance.candidato.nome} tem {instance.score}% de compatibilidade com sua vaga "{instance.vaga.titulo}"',
                url=f'/dashboard_empresa/'
            )
    except Exception:
        pass


@receiver(post_save, sender=Candidatura)
def criar_notificacao_candidatura(sender, instance, created, **kwargs):
    """Cria notificação quando uma candidatura é criada ou atualizada"""
    if created:
        try:
            if instance.vaga.empresa.user:
                Notificacao.objects.create(
                    usuario=instance.vaga.empresa.user,
                    tipo='candidatura',
                    titulo='Nova Candidatura Recebida!',
                    mensagem=f'{instance.candidato.nome} se candidatou para a vaga "{instance.vaga.titulo}"',
                    url=f'/dashboard_empresa/'
                )
        except Exception:
            pass
    else:
        try:
            if instance.candidato.user and instance.status != 'pendente':
                status_texto = dict(instance.STATUS_CHOICES).get(instance.status, instance.status)
                Notificacao.objects.create(
                    usuario=instance.candidato.user,
                    tipo='candidatura',
                    titulo='Atualização de Candidatura',
                    mensagem=f'Sua candidatura para "{instance.vaga.titulo}" está: {status_texto}',
                    url=f'/candidaturas/'
                )
        except Exception:
            pass


@receiver(post_save, sender=Mensagem)
def criar_notificacao_mensagem(sender, instance, created, **kwargs):
    """Cria notificação quando uma nova mensagem é enviada"""
    if not created:
        return
    
    try:
        if instance.destinatario:
            Notificacao.objects.create(
                usuario=instance.destinatario,
                tipo='mensagem',
                titulo='Nova Mensagem Recebida',
                mensagem=f'{instance.remetente.username} enviou: "{instance.assunto}"',
                url='/mensagens/'
            )
    except Exception:
        pass
