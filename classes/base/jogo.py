class Jogo():
    def __init__(self, estado = None, turno = None):
        self.estado = estado
        self.turno = turno

    def turno(self):
        raise NotImplementedError("Deve ser implementado!")

    def jogar(self, jogada):
        raise NotImplementedError("Deve ser implementado!")

    def jogadas_validas(self):
        raise NotImplementedError("Deve ser implementado!")

    def venceu(self):
        raise NotImplementedError("Deve ser implementado!")

    def empate(self):
        raise NotImplementedError("Deve ser implementado!")

    def calcular_utilidade(self):
        raise NotImplementedError("Deve ser implementado!")

    def imprimir(self):
        raise NotImplementedError("Deve ser implementado!")

    def imprimir_jogada(self, turno, jogada):
        raise NotImplementedError("Deve ser implementado!")

