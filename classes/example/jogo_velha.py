from enum import Enum
from jogo import Jogador, Jogo
from minimax import melhor_jogada_agente, melhor_jogada_agente_poda

class Quadrado(Jogador, Enum):
    X = "X"
    O = "O"
    V = " " # vazio

    def oposto(self):
        if self == Quadrado.X:
            return Quadrado.O
        elif self == Quadrado.O:
            return Quadrado.X
        else:
            return Quadrado.V

    def __str__(self):
        return self.value

class JogoVelha(Jogo):
    def __init__(self, posicao = [Quadrado.V] * 9, turno = Quadrado.X):
        self.posicao = posicao
        self._turno = turno

    def turno(self):
        return self._turno
    
    def jogar(self, local):
        temp = self.posicao.copy()
        temp[local] = self._turno
        return JogoVelha(temp, self.turno().oposto())

    def jogos_validos(self):
        return [p for p in range(len(self.posicao)) if self.posicao[p] == Quadrado.V]
    
    def venceu(self):
        return self._venceu_linhas(self.posicao) or self._venceu_colunas(self.posicao) or self._venceu_diagonal(self.posicao) 

    def _venceu_linhas(self, posicao):
        return posicao[0] == posicao[1] and posicao[0] == posicao[2] and posicao[0] != Quadrado.V or \
        posicao[3] == posicao[4] and posicao[3] == posicao[5] and posicao[3] != Quadrado.V or \
        posicao[6] == posicao[7] and posicao[6] == posicao[8] and posicao[6] != Quadrado.V

    def _venceu_colunas(self, posicao):
        return posicao[0] == posicao[3] and posicao[0] == posicao[6] and posicao[0] != Quadrado.V or \
        posicao[1] == posicao[4] and posicao[1] == posicao[7] and posicao[1] != Quadrado.V or \
        posicao[2] == posicao[5] and posicao[2] == posicao[8] and posicao[2] != Quadrado.V

    def _venceu_diagonal(self, posicao):
        return posicao[0] == posicao[4] and posicao[0] == posicao[8] and posicao[0] != Quadrado.V or \
        posicao[2] == posicao[4] and posicao[2] == posicao[6] and posicao[2] != Quadrado.V

    def calcular_utilidade(self, jogador):
        if self.venceu() and self._turno == jogador:
            return -1
        elif self.venceu() and self._turno != jogador:
            return 1
        else:
            return 0

    def __str__(self):
        return f"""{self.posicao[0]}|{self.posicao[1]}|{self.posicao[2]}
-----
{self.posicao[3]}|{self.posicao[4]}|{self.posicao[5]}
-----
{self.posicao[6]}|{self.posicao[7]}|{self.posicao[8]}"""

jogo = JogoVelha()

def jogada_humano():
    jogada = -1
    while jogada not in jogo.jogos_validos():
        jogada = int(input("Escolha um quadrado (0-8):"))
    return jogada

if __name__ == "__main__":
    while True:
        humano = jogada_humano()
        jogo = jogo.jogar(humano)
        if jogo.venceu():
            print("Humano Venceu!")
            break
        elif jogo.empate():
            print("Empate!")
            break
        computador = melhor_jogada_agente(jogo)
        print(f"Jogada do Computador é {computador}")
        jogo = jogo.jogar(computador)
        print(jogo)
        if jogo.venceu():
            print("Computador venceu!")
            break
        elif jogo.empate():
            print("Empate!")
            break
