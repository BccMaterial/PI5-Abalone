from copy import deepcopy
from classes.base.jogada import Jogada

class JogadaAbalone(Jogada):
    def __init__(self, posicao: tuple, direcao: str, jogador: int):
        self.posicao = posicao
        self.direcao = direcao
        self.jogador = jogador

    def e_valida(self, jogo):
        # print(f"resultado calcular_pos: {jogo.calcular_pos(self.posicao, self.direcao)}")
        # print(f"resultado get_estado: {jogo.get_estado(self.posicao)}")
        # print(f"direcao: {self.direcao}")
        jogo_copy = deepcopy(jogo)
        movimento_resultado = jogo_copy.movimentar_peca(self.posicao, self.direcao)
        return \
            jogo.calcular_pos(self.posicao, self.direcao) is not None and \
            jogo.get_estado(self.posicao) == jogo.turno() and \
            self.direcao in jogo.direcoes_possiveis and \
            movimento_resultado != 1

    def imprimir_jogada(self):
        print(f"Jogador {self.jogador} moveu a peça {self.posicao} na direção {self.direcao}")
