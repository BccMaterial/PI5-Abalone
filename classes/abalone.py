class Abalone:
    def init(self):
        self.tabuleiro = self.criarTabuleiro() #Cria o Tabuleiro
        self.turnoJogador= 1 #Define se é o turno do jogador 1 ou 2
        self.pecasDerrubadas= {1: 0, 2: 0} #1 se refere ao primeiro jogador e quantas peças ele perdeu. 2 se refere ao segundo jogador e quantas pecas ele perdeu
    def criarTabuleiro(self):
        #Implementar função

        return [] #1 e 2 são utilizados para representar os espaços ocupados pelas peças dos jogadores e None é utilizado para representar os espaços não ocupados

    def movimentarPecas(self, posicaoJogador, direcao):
        #Implementar função
        pass

    def empurrarOponente(self):
        #Implementar função
        pass

    def checarVitoria(self):
        return self.pecasDerrubadas[1] >= 6 or self.pecasDerrubadas[2]>=6 #Checa os valores associados as Keys do dicionário, e, caso qualquer um deles seja maior ou igual a 6, temos um vencedor

    def imprimirTabuleiro(self): #Implementar
        for linha in self.tabuleiro:
            print() #Se o elemento do array for 1 ou 2, transformar o mesmo em uma string, concatena-los e printar na tela. Caso o elemento do array esteja vazio, fazer o mesmo utilizando um "." para representar o vazio no tabuleiro

    def jogar(self):
        self.imprimirTabuleiro()
        print(f"Turno do jogador {self.turnoJogador}")
        #implementar
        self.turnoJogador = 3 -self.turnoJogador #Utilizado para alternar entre o player 1 e 2. Também temos que determinar a maneira de escolher quem será o jogador 1 e 2
