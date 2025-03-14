class Abalone:
    def __init__(self):
        self.tabuleiro = self.criar_tabuleiro()
        self.turno_jogador= 1
        # 1 -> Pontuação primeiro jogador
        # 2 -> Pontuação segundo jogador
        self.pecas_derrubadas= {
            1: 0, 
            2: 0
        }

    # 1 e 2 são utilizados para representar os espaços ocupados pelas peças 
    # dos jogadores e None é utilizado para representar os espaços não ocupados
    def criar_tabuleiro(self):
        # Baseado em relação a este tabuleiro: https://www.divertivida.com.br/abalone-classic
        # Representação do tabuleiro:
        #
        #     2 2 2 2 2
        #    2 2 2 2 2 2
        #   - - 2 2 2 - -
        #  - - - - - - - -
        # - - - - - - - - -
        #  - - - - - - - -
        #   - - 1 1 1 - - 
        #    1 1 1 1 1 1
        #     1 1 1 1 1
        #
        return [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2,],
        ]

    def movimentar_pecas(self, posicao_jogador, direcao):
        # Implementar função
        pass

    def empurrar_oponente(self):
        #Implementar função
        pass

    def checar_vitoria(self):
        # Checa os valores associados as Keys do dicionário, 
        # e caso qualquer um deles seja maior ou igual a 6, temos um vencedor
        return self.pecas_derrubadas[1] >= 6 or self.pecas_derrubadas[2]>=6

    def imprimir_tabuleiro(self):
        tamanho_maximo = len(max(self.tabuleiro, key=len))
        str_final = ""
        str_final += "\n"
        for linha in self.tabuleiro:
            quantidade_espaços = tamanho_maximo - len(linha)
            str_final += "".join(" " for x in range(quantidade_espaços))
            str_final += " ".join([str(i) for i in linha])
            str_final += "\n"
        print(str_final)

    def jogar(self):
        self.imprimir_tabuleiro()
        print(f"Turno do jogador {self.turno_jogador}")
        # TODO: Implementar
        # Utilizado para alternar entre o player 1 e 2. Também temos que determinar 
        # a maneira de escolher quem será o jogador 1 e 2
        self.turno_jogador = 3 - self.turno_jogador
