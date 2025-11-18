"""
Sistema de Matching entre Candidatos e Vagas
Calcula compatibilidade baseado em múltiplos fatores
"""
from .models import Candidato, Vaga, Match


def calcular_score_habilidades(candidato_habilidades, vaga_habilidades):
    """
    Calcula score baseado na compatibilidade de habilidades
    Retorna: 0-40 pontos
    """
    if not candidato_habilidades or not vaga_habilidades:
        return 0
    
    candidato_set = set([h.strip().lower() for h in candidato_habilidades.split(',')])
    vaga_set = set([h.strip().lower() for h in vaga_habilidades.split(',')])
    
    if not vaga_set:
        return 0
    
    # Calcula porcentagem de habilidades que o candidato possui
    habilidades_match = candidato_set.intersection(vaga_set)
    porcentagem = (len(habilidades_match) / len(vaga_set)) * 100
    
    # Máximo de 40 pontos para habilidades
    return min(int(porcentagem * 0.4), 40)


def calcular_score_experiencia(candidato_anos, vaga_anos_min):
    """
    Calcula score baseado na experiência
    Retorna: 0-20 pontos
    """
    if candidato_anos >= vaga_anos_min:
        # Se tem a experiência mínima ou mais, dá pontuação cheia
        return 20
    elif candidato_anos >= (vaga_anos_min * 0.7):
        # Se tem 70% da experiência necessária, dá pontuação parcial
        return 15
    elif candidato_anos >= (vaga_anos_min * 0.5):
        # Se tem 50% da experiência necessária
        return 10
    else:
        # Pouca experiência
        return 5


def calcular_score_localizacao(candidato_cidade, candidato_estado, vaga_cidade, vaga_estado, vaga_tipo):
    """
    Calcula score baseado na localização
    Retorna: 0-20 pontos
    """
    # Se for remoto, localização não importa
    if vaga_tipo == 'remoto':
        return 20
    
    # Mesma cidade: pontuação máxima
    if candidato_cidade.lower() == vaga_cidade.lower():
        return 20
    
    # Mesmo estado: pontuação média
    if candidato_estado.lower() == vaga_estado.lower():
        return 15
    
    # Híbrido e em outro estado
    if vaga_tipo == 'hibrido':
        return 5
    
    # Presencial e em outra localização
    return 0


def calcular_score_salario(candidato_pretensao, vaga_salario_min, vaga_salario_max):
    """
    Calcula score baseado na compatibilidade salarial
    Retorna: 0-20 pontos
    """
    if not candidato_pretensao or not vaga_salario_min:
        return 10  # Score neutro se não houver informação
    
    # Se a pretensão está dentro da faixa da vaga
    if vaga_salario_max and vaga_salario_min <= candidato_pretensao <= vaga_salario_max:
        return 20
    
    # Se a pretensão está próxima (até 20% acima do máximo)
    if vaga_salario_max and candidato_pretensao <= vaga_salario_max * 1.2:
        return 15
    
    # Se a pretensão está até o salário mínimo + 50%
    if candidato_pretensao <= vaga_salario_min * 1.5:
        return 10
    
    # Pretensão muito alta
    return 5


def calcular_compatibilidade(candidato, vaga):
    """
    Calcula o score total de compatibilidade entre candidato e vaga
    Retorna: 0-100
    """
    score_total = 0
    
    # Habilidades (40 pontos)
    score_total += calcular_score_habilidades(
        candidato.habilidades,
        vaga.habilidades_necessarias
    )
    
    # Experiência (20 pontos)
    score_total += calcular_score_experiencia(
        candidato.experiencia_anos,
        vaga.experiencia_minima
    )
    
    # Localização (20 pontos)
    score_total += calcular_score_localizacao(
        candidato.cidade,
        candidato.estado,
        vaga.cidade,
        vaga.estado,
        vaga.tipo
    )
    
    # Salário (20 pontos)
    score_total += calcular_score_salario(
        candidato.pretensao_salarial,
        vaga.salario_min,
        vaga.salario_max
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
