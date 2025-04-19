class Jogador:
    def oposto(self):
        raise NotImplementedError("Deve ser implementado")

class Jogo():
    def turno(self):
        pass

    def jogar(self, localizacao):
        pass

    def jogos_validos(self):
        pass

    def venceu(self):
        pass

    def empate(self):
        return (not self.venceu()) and (len(self.jogos_validos()) == 0)

    def avaliar(self, player):
        pass


