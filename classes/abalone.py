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
        # O -1 é pra compensar os tamanhos das listas (vai facilitar na hora de mover)
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

    # Get e set compatível com tuplas
    def get_tabuleiro(self, pos: tuple):
        linha, coluna = pos
        return self.tabuleiro[linha][coluna]

    def set_tabuleiro(self, pos: tuple, valor: int):
        linha, coluna = pos
        self.tabuleiro[linha][coluna] = valor

    def movimentar_peca(self, peca_pos: tuple, direcao: str):
        """
        Observações:
        - peca_pos é formada por: (linha, coluna)
        """        
        pos_atual = peca_pos
        proxima_pos = self.calcular_pos(pos_atual, direcao.lower())
        
        if proxima_pos is None:
            # print("Posição selecionada inválida!")
            return

        self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
        self.set_tabuleiro(pos_atual, 0)

    def posicao_valida(self, pos: tuple):
        max_linha = len(self.tabuleiro) - 1
        linha_escolhida = self.tabuleiro[pos[0]]
        max_coluna = len([x for x in linha_escolhida]) - 1
        valor_pos = self.get_tabuleiro(pos)
        return \
            valor_pos == 0 and \
            pos[0] <= max_linha and \
            pos[1] <= max_coluna and \
            pos[1] >= 0

    def calcular_pos(self, pos: tuple, direcao: str):
        """
        Função para pegar a posição seguinte com base na posição e na direção inserida.

        > Retornará `None` caso seja uma posição inválida
        """

        movimentos = {
            "e": (pos[0], pos[1] - 1), # Continua na linha, volta uma coluna
            "d": (pos[0], pos[1] + 1), # Continua na mesma linha, anda uma coluna
            "ce": (pos[0] - 1, pos[1] - 1), # Diminui uma linha, volta uma coluna
            "cd": (pos[0] - 1, pos[1]), # Diminui uma linha, anda uma coluna
            "be": (pos[0] + 1, pos[1] - 1), # Aumenta uma linha, volta uma coluna
            "bd": (pos[0] + 1, pos[1]) # Aumenta uma linha, anda uma coluna
        }

        linha_atual_len = len(self.tabuleiro[pos[0]])
        proxima_pos = movimentos[direcao]
        prox_linha = proxima_pos[0]
        prox_linha_len = len(self.tabuleiro[prox_linha])
        linha_atual_len = len(self.tabuleiro[pos[0]])
        diff_len = linha_atual_len - prox_linha_len
        if diff_len >= 1:
            diff_len -= 1
        proxima_pos = (proxima_pos[0], proxima_pos[1] - diff_len)

        if not self.posicao_valida(proxima_pos):
            return None

        return proxima_pos

    def empurrar_oponente(self, pecas: list, direcao: str):

        # Sumito: Para poder empurrar uma peça do adversário, deve se assumir uma posição de "sumito"
        # Para que se possa entrar em sumito, a sua quantidade de esferas deve ser maior do que a do seu oponente
        # A sua quantidade de esferas para entrar em sumito deve ser 2 ou 3
        # Exemplo: é necessário que existe duas esferas alinhadas suas para poder empurrar uma peça adversária para tras

        # Para que o sumito possa ocorrer, é necessário que o jogador tenha 2 ou 3 peças alinhadas
        if(len(pecas) >= 3 and len(pecas) <= 2): 
            print("Precisa de 2 ou 3 peças alinhadas")
            return False

        # Encontra a posição atual do jogador
        pos_jogador = self.get_tabuleiro(pecas[0]) 

        # Tupla da peça do oponente mais próxima
        pos_oponente = self.calcular_pos(pecas[-1], direcao)

        if not (0 <= pos_oponente[0] < len(self.tabuleiro) and 0 <= pos_oponente[1] < len(self.tabuleiro[pos_oponente[0]])): #Verifica se a linha do oponente é valida e se o valor da coluna do oponente é menor que o valor da linha do mesmo
            print("Sem peças oponentes nesta direção para empurrar")
            return False

        # Verifica se existe uma peça para empurrar a frente
        if self.get_tabuleiro(pos_oponente) == 0 or self.get_tabuleiro(pos_oponente) == pos_jogador: 
            print("Não existe nenhuma peça do oponente a frente para empurrar")

    def testar_objetivo(self):
        return self.pecas_derrubadas[1] >= 6 or self.pecas_derrubadas[2] >= 6

    def imprimir_tabuleiro(self):
        tamanho_maximo = len(max(self.tabuleiro, key=len))
        str_final = ""
        str_final += f" \t{" ".join(str(i) for i in range(tamanho_maximo))}\n"
        str_final += "\n"
        for i, linha in enumerate(self.tabuleiro):
            quantidade_espaços = tamanho_maximo - len(linha)
            str_final += f"{i}\t"
            str_final += "".join(" " for _ in range(quantidade_espaços))
            str_final += " ".join([str(i) for i in linha])
            str_final += "\n"
        print(str_final)

    def jogar(self):
        # O usuário vai inserir as coordenadas da peça. ("Linha, Coluna") Ex: 0, 3
        # Temos que pegar a diferença entre a lista com maior tamanho e a lista que ele escolheu
        ultimo_input = ""
        while not self.testar_objetivo():
            self.imprimir_tabuleiro()
            print("Instruções")
            print("----------------------------------")
            print("- Insira a coordenada da peça que você deseja mover -> \"NLinha, NColuna\"")
            print("- Caso queira sair, digite q")
            print(f"Turno do jogador {self.turno_jogador}")

            pos_valida = False
            while not pos_valida:
                ultimo_input = input("Digite as coordenadas (NLinha, NColuna): ")
                if ultimo_input == "q":
                    return

                pos_inserida = tuple([int(x) for x in ultimo_input.split(", ")])

                if self.get_tabuleiro(pos_inserida) != self.turno_jogador:
                    print("A peça selecionada é do outro jogador! Por favor, selecione outra.")
                else:
                    pos_valida = True


            print("Possíveis direções:")
            print("e -> esquerda")
            print("d -> direita")
            print("ce -> diagonal cima esquerda")
            print("cd -> diaconal cima direita")
            print("be -> diagonal baixo esquerda")
            print("bd -> diagonal baixo direita")
            ultimo_input = input("Agora, digite a direção: ")

            if ultimo_input == "q":
                break

            direcao = ultimo_input

            self.movimentar_peca(pos_inserida, direcao)

            # Alterna o turno
            self.turno_jogador = 3 - self.turno_jogador
