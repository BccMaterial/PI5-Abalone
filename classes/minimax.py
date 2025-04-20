def minimax(jogo, turno_max: bool, jogador, profundidade_maxima = 8):
  # se o jogo acabou ou se a profundidade é máxima
  if jogo.venceu() or profundidade_maxima == 0:
    return jogo.calcular_utilidade(jogador)

  if turno_max: # turno do MAX
    melhor_valor = float("-inf") # Menos infinito é o menor valor
    for proxima_jogada in jogo.jogadas_validas():
      utilidade = minimax(jogo.jogar(proxima_jogada), False, jogador, profundidade_maxima - 1)
      melhor_valor = max(utilidade, melhor_valor) # proximo_jogo com o maior valor
    return melhor_valor
  else: # turno no MIN
    pior_valor = float("inf") # Mais infinito é o maior valor
    for proxima_jogada in jogo.jogadas_validas():
      utilidade = minimax(jogo.jogar(proxima_jogada), True, jogador, profundidade_maxima - 1)
      pior_valor = min(utilidade, pior_valor) # proximo_jogo com o menor valor
    return pior_valor

def minimax_alfabeta(jogo, turno_max: bool, jogador, profundidade_maxima = 8, alfa = float("-inf"), beta = float("inf")):
  # se o jogo acabou ou se a profundidade é máxima
  if jogo.venceu() or profundidade_maxima == 0:
    return jogo.calcular_utilidade(jogador)

  if turno_max: # turno do MAX
    for proxima_jogada in jogo.jogadas_validas():
      utilidade = minimax_alfabeta(jogo.jogar(proxima_jogada), False, jogador, profundidade_maxima - 1, alfa, beta)
      alfa = max(utilidade, alfa)
      if beta <= alfa:
        continue
      return alfa
  else: # turno no MIN
    for proxima_jogada in jogo.jogadas_validas():
      utilidade = minimax_alfabeta(jogo.jogar(proxima_jogada), True, jogador, profundidade_maxima - 1, alfa, beta)
      beta = min(utilidade, beta)
      if beta <= alfa:
        continue
      return beta

# Encotrar o melhor movimento do computador
def melhor_jogada_agente(jogo, profundidade_maxima = 8):
  melhor_valor = float("-inf")
  melhor_jogada = -1
  for proxima_jogada in jogo.jogadas_validas():
    utilidade = minimax(jogo.jogar(proxima_jogada), False, jogo.turno(), profundidade_maxima)
    if utilidade > melhor_valor:
      melhor_valor = utilidade
      melhor_jogada = proxima_jogada
  return melhor_jogada

def melhor_jogada_agente_poda(jogo, profundidade_maxima = 8):
  melhor_valor = float("-inf")
  melhor_jogada = -1
  for proxima_jogada in jogo.jogadas_validas():
    utilidade = minimax_alfabeta(jogo.jogar(proxima_jogada), False, jogo.turno(), profundidade_maxima)
    if utilidade > melhor_valor:
      melhor_valor = utilidade
      melhor_jogada = proxima_jogada
  return melhor_jogada

