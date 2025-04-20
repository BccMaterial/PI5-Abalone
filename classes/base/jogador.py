from classes.minimax import minimax_alfabeta

class Jogador:
    def __init__(self, identificador, min_max = None):
        self.identificador = identificador
        self.min_max = min_max

    def define_proximo_turno(self, proximo_turno):
        self.jogador_proximo_turno = proximo_turno

    def imprimir(self):
        return self.identificador

    def jogar(self, jogo):
        raise NotImplementedError("Deve ser implementado!")

    def e_min(self):
        return self.min_max == "min"

    def e_max(self):
        return self.min_max == "max"

    def proximo_turno(self):
        return self.jogador_proximo_turno

class JogadorHumano(Jogador):
    def __init__(self, identificador):
        super().__init__(identificador, "min")

class JogadorAgente(Jogador):
    def __init__(self, identificador):
        super().__init__(identificador, "max")

    def jogar(self, jogo):
        profundidade_maxima = 8
        melhor_valor = float("-inf")
        melhor_jogada = -1
        print(jogo.turno().imprimir())
        for proximo_jogo in jogo.gerar_jogadas_validas():
            utilidade = minimax_alfabeta(jogo.jogar(proximo_jogo), jogo.turno(), profundidade_maxima)
            if utilidade > melhor_valor:
                melhor_valor = utilidade
                melhor_jogada = proximo_jogo
        return melhor_jogada
