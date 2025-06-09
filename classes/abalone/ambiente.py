import numpy as np
from copy import deepcopy
from classes.base.ambiente import Ambiente

class AbaloneAmbiente(Ambiente):
    def __init__(self, jogo, jogador, jogador_agente):
        self.jogo = jogo  # Guarda o objeto do jogo
        self.jogador = jogador  # Jogador atual (1 ou 2)
        self.jogador_agente = jogador_agente
        
        # Lista de direções possíveis (6 no total)
        self.estados = np.array([jogo])
        
        # Ações serão geradas dinamicamente com base em jogadas válidas
        self.acoes = self._gerar_acoes()  # Lista de ações válidas no estado atual

        if self.jogador == self.jogador_agente.identificador:
            raise ValueError("O jogador Q-Learning deve ser diferente do Jogador Minimax!")

    def _gerar_acoes(self, jogo = None):
        if jogo is not None:
            acoes_validas = []
            for jogada in jogo.jogadas_validas():
                acoes_validas.append((jogada.posicao, jogada.direcao))
            self.n_acoes = len(acoes_validas)
            return acoes_validas

        acoes_validas = []
        for jogada in self.jogo.jogadas_validas():
            acoes_validas.append((jogada.posicao, jogada.direcao))
    
        self.n_acoes = len(acoes_validas)
        return np.array(acoes_validas, dtype=object)

    def T(self, estado, acao):
        if self.jogo.turno() != self.jogador:
            self.jogador_agente.jogar(self.jogo)
            self._gerar_acoes()

        if estado >= len(self.estados):
            raise ValueError("Estado inválido.")
    
        direcoes_possiveis = self.jogo.direcoes_possiveis
        estado_atual = self.estados[estado]
        proximas_acoes = self._gerar_acoes(estado_atual)
        
        if acao < 0 or acao >= len(proximas_acoes):
            raise ValueError("Ação inválida.")
        
        pos, direcao = proximas_acoes[acao]
        dir_i = direcoes_possiveis.index(direcao)
        aux_self_jogo = deepcopy(self.jogo)
        proximo_estado = self.jogo
        proximo_estado.movimentar_peca(pos, direcao)
        proximo_estado_v = (pos[0] + pos[1] + 2) * dir_i
        transicoes = [(proximo_estado_v, 0.6)]
        
        # Ações restantes
        acoes_alternativas = list(proximas_acoes)
        del acoes_alternativas[acao]
        prob_alternativos = 0.4 / len(acoes_alternativas)

        for acao in acoes_alternativas:
            proximo_estado = deepcopy(aux_self_jogo)    
            pos, direcao = acao
            dir_i = direcoes_possiveis.index(direcao)
            proximo_estado.movimentar_peca(pos, direcao)
            proximo_estado_v = (pos[0] + pos[1] + 2) * dir_i
            transicoes.append((proximo_estado_v, prob_alternativos))
        
        return transicoes

    def R(self, estado, acao, proximo_estado):
        recompensa = 0
        
        # Verifica se houve captura de peça adversária

        estado_atual = self.estados[estado]
        estado_proximo = self.estados[proximo_estado]
        placar_antes = estado_atual.placar
        placar_depois = estado_proximo.placar
        
        if placar_depois[self.jogador] > placar_antes[self.jogador]:
            recompensa += 1  # Recompensa por capturar peça
        
        # Penaliza se o jogador perdeu uma peça
        adversario = 3 - self.jogador  # Inimigo (1 → 2, 2 → 1)
        if placar_depois[adversario] > placar_antes[adversario]:
            recompensa -= 1
        
        # Recompensa por avançar em direção ao centro
        utilidade_antes = estado_atual.calcular_utilidade(self.jogador)
        utilidade_depois = estado_proximo.calcular_utilidade(self.jogador)
        recompensa += 0.5 * (utilidade_depois - utilidade_antes)
        return recompensa

    def __str__(self):
        return str(self.jogo)

    def estado_final(self, estado):
        return self.estados[estado].venceu()

    def imprimir_valor(self, V):
        print("Valores estimados para cada estado:")
        for estado, valor in V.items():
            print(f"Estado: {estado} → Valor: {valor}")

    def imprimir_politica(self, politica):
        print("Política ótima:")
        for estado, acao in politica.items():
            print(f"Estado: {estado} → Ação: {self.acoes[acao]}")
