from classes.base.jogada import Jogada

class JogadaAbalone(Jogada):
    def __init__(self, posicao: tuple, direcao: str):
        self.posicao = posicao
        self.direcao = direcao

    def e_valida(self, jogo):
        return \
            jogo.calcular_pos(self.posicao, self.direcao) is not None and \
            jogo.get_estado(self.posicao) == jogo.turno() and \
            self.direcao in jogo.direcoes_possiveis
