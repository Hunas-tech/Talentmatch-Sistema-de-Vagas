"""
Sistema de Matching entre Candidatos e Vagas
Calcula compatibilidade baseado em múltiplos fatores com pesos configuráveis
"""
from django.conf import settings
from .models import Candidato, Vaga, Match

def get_matching_weights():
    """Obtém os pesos de matching das configurações do Django com validação"""
    defaults = {
        'habilidades': 40,
        'experiencia': 25,
        'localizacao': 20,
        'salario': 15,
    }
    
    weights = getattr(settings, 'MATCHING_WEIGHTS', {})
    
    result = {}
    for key in defaults:
        value = weights.get(key, defaults[key])
        if not isinstance(value, (int, float)) or value < 0 or value > 100:
            result[key] = defaults[key]
        else:
            result[key] = value
    
    return result


def calcular_score_habilidades(candidato_habilidades, vaga_habilidades, peso_maximo=40):
    """
    Calcula score baseado na compatibilidade de habilidades
    Retorna: 0-40 pontos
    """
    if not candidato_habilidades or not vaga_habilidades:
        return 0
    
    # Filtra strings vazias antes de criar os sets
    candidato_set = set([h.strip().lower() for h in candidato_habilidades.split(',') if h.strip()])
    vaga_set = set([h.strip().lower() for h in vaga_habilidades.split(',') if h.strip()])
    
    if not vaga_set or not candidato_set:
        return 0
    
    # Calcula porcentagem de habilidades que o candidato possui
    habilidades_match = candidato_set.intersection(vaga_set)
    porcentagem = (len(habilidades_match) / len(vaga_set)) * 100
    
    # Retorna score proporcional ao peso máximo
    return min(int(porcentagem * peso_maximo / 100), peso_maximo)


def calcular_score_experiencia(candidato_anos, vaga_anos_min, peso_maximo=25):
    """
    Calcula score baseado na experiência
    Retorna: 0-25 pontos (peso configurável)
    """
    if candidato_anos >= vaga_anos_min:
        return peso_maximo
    elif candidato_anos >= (vaga_anos_min * 0.7):
        return int(peso_maximo * 0.75)
    elif candidato_anos >= (vaga_anos_min * 0.5):
        return int(peso_maximo * 0.5)
    else:
        return int(peso_maximo * 0.2)


def calcular_score_localizacao(candidato_cidade, candidato_estado, vaga_cidade, vaga_estado, vaga_tipo, peso_maximo=20):
    """
    Calcula score baseado na localização
    Retorna: 0-20 pontos (peso configurável)
    """
    if vaga_tipo == 'remoto':
        return peso_maximo
    
    candidato_cidade = (candidato_cidade or '').strip()
    candidato_estado = (candidato_estado or '').strip()
    vaga_cidade = (vaga_cidade or '').strip()
    vaga_estado = (vaga_estado or '').strip()
    
    if candidato_cidade and vaga_cidade and candidato_cidade.lower() == vaga_cidade.lower():
        return peso_maximo
    
    if candidato_estado and vaga_estado and candidato_estado.lower() == vaga_estado.lower():
        return int(peso_maximo * 0.75)
    
    if vaga_tipo == 'hibrido':
        return int(peso_maximo * 0.25)
    
    return 0


def calcular_score_salario(candidato_pretensao, vaga_salario_min, vaga_salario_max, peso_maximo=15):
    """
    Calcula score baseado na compatibilidade salarial
    Retorna: 0-15 pontos (peso configurável)
    """
    if not candidato_pretensao or not vaga_salario_min:
        return int(peso_maximo * 0.5)
    
    candidato_pretensao = float(candidato_pretensao)
    vaga_salario_min = float(vaga_salario_min)
    vaga_salario_max = float(vaga_salario_max) if vaga_salario_max else None
    
    # Se a pretensão está dentro da faixa da vaga
    if vaga_salario_max and vaga_salario_min <= candidato_pretensao <= vaga_salario_max:
        return peso_maximo
    
    # Se a pretensão está próxima (até 20% acima do máximo)
    if vaga_salario_max and candidato_pretensao <= vaga_salario_max * 1.2:
        return int(peso_maximo * 0.75)
    
    # Se a pretensão está até o salário mínimo + 50%
    if candidato_pretensao <= vaga_salario_min * 1.5:
        return int(peso_maximo * 0.5)
    
    return int(peso_maximo * 0.2)


def calcular_compatibilidade(candidato, vaga, pesos=None):
    """
    Calcula o score total de compatibilidade entre candidato e vaga
    Retorna: 0-100
    """
    if pesos is None:
        pesos = get_matching_weights()
    
    score_total = 0
    
    score_total += calcular_score_habilidades(
        candidato.habilidades,
        vaga.habilidades_necessarias,
        peso_maximo=pesos['habilidades']
    )
    
    score_total += calcular_score_experiencia(
        candidato.experiencia_anos,
        vaga.experiencia_minima,
        peso_maximo=pesos['experiencia']
    )
    
    score_total += calcular_score_localizacao(
        candidato.cidade,
        candidato.estado,
        vaga.cidade,
        vaga.estado,
        vaga.tipo,
        peso_maximo=pesos['localizacao']
    )
    
    score_total += calcular_score_salario(
        candidato.pretensao_salarial,
        vaga.salario_min,
        vaga.salario_max,
        peso_maximo=pesos['salario']
    )
    
    return min(score_total, 100)


def gerar_matches_para_candidato(candidato_id, score_minimo=50):
    """
    Gera matches para um candidato específico
    Retorna lista de matches ordenados por score
    """
    try:
        candidato = Candidato.objects.get(id=candidato_id)
    except Candidato.DoesNotExist:
        return []
    
    # Busca vagas abertas
    vagas_abertas = Vaga.objects.filter(status='aberta')
    
    matches = []
    for vaga in vagas_abertas:
        # Verifica se já existe match
        match_existente = Match.objects.filter(
            candidato=candidato,
            vaga=vaga
        ).first()
        
        if match_existente:
            # Atualiza o score do match existente
            score = calcular_compatibilidade(candidato, vaga)
            match_existente.score = score
            match_existente.save()
            matches.append(match_existente)
        else:
            # Calcula compatibilidade
            score = calcular_compatibilidade(candidato, vaga)
            
            # Só cria match se score for maior que o mínimo
            if score >= score_minimo:
                match = Match.objects.create(
                    candidato=candidato,
                    vaga=vaga,
                    score=score
                )
                matches.append(match)
    
    # Ordena por score (maior primeiro)
    matches.sort(key=lambda x: x.score, reverse=True)
    return matches


def gerar_matches_para_vaga(vaga_id, score_minimo=50):
    """
    Gera matches para uma vaga específica
    Retorna lista de matches ordenados por score
    """
    try:
        vaga = Vaga.objects.get(id=vaga_id)
    except Vaga.DoesNotExist:
        return []
    
    # Busca todos os candidatos
    candidatos = Candidato.objects.all()
    
    matches = []
    for candidato in candidatos:
        # Verifica se já existe match
        match_existente = Match.objects.filter(
            candidato=candidato,
            vaga=vaga
        ).first()
        
        if match_existente:
            # Atualiza o score
            score = calcular_compatibilidade(candidato, vaga)
            match_existente.score = score
            match_existente.save()
            matches.append(match_existente)
        else:
            # Calcula compatibilidade
            score = calcular_compatibilidade(candidato, vaga)
            
            # Só cria match se score for maior que o mínimo
            if score >= score_minimo:
                match = Match.objects.create(
                    candidato=candidato,
                    vaga=vaga,
                    score=score
                )
                matches.append(match)
    
    # Ordena por score (maior primeiro)
    matches.sort(key=lambda x: x.score, reverse=True)
    return matches


def recalcular_todos_matches():
    """
    Recalcula scores de todos os matches existentes
    """
    matches = Match.objects.all()
    atualizado = 0
    
    for match in matches:
        novo_score = calcular_compatibilidade(match.candidato, match.vaga)
        if match.score != novo_score:
            match.score = novo_score
            match.save()
            atualizado += 1
    
    return atualizado
