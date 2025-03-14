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
            [-1, -1, -1, -1, 1, 1, 1, 1, 1],
            [-1, -1, -1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 0, 0, 1, 1, 1, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, 0, 0, 2, 2, 2, 0, 0],
            [-1, -1, -1, 2, 2, 2, 2, 2, 2],
            [-1, -1, -1, -1, 2, 2, 2, 2, 2,],
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
        - peca_jogador é formada por: (linha, coluna)

        Movimentos:
        - e -> (linha, coluna-1)
        - d -> (linha, coluna+1)
        - ce -> (linha-1, coluna-1)
        - cd -> (linha-1, coluna)
        - bd -> (linha+1, coluna+1)
        - be -> (linha+1, coluna)        
        """
        
        ########################
        ### FUNÇÃO VALIDAÇÃO ###
        ########################

        def posicao_valida(pos: tuple):
            max_linha = len(self.tabuleiro) - 1
            # Se -1 -1 -1 0 0 2 2 0 0
            # Pos -> 3-8
            linha_escolhida = self.tabuleiro[pos[0]]
            max_coluna = len([x for x in linha_escolhida]) - 1
            min_coluna = len([x for x in linha_escolhida if x == -1]) + 1
            valor_pos = self.get_tabuleiro(pos)
            return \
                valor_pos == 0 and \
                pos[0] <= max_linha and \
                pos[1] <= max_coluna and \
                pos[1] >= min_coluna

        ################
        ### DIREÇÕES ###
        ################
        # Obs: Não me pergunte por que os + e - dos movimentos,
        # Só sei que fui testando e funcionou
        # e -> (linha, coluna-1)
        # d -> (linha, coluna+1)
        # ce -> (linha-1, coluna-1)
        # cd -> (linha-1, coluna)
        # bd -> (linha+1, coluna+1)
        # be -> (linha+1, coluna)

        def esquerda():
            pos_atual = peca_pos
            proxima_pos = (peca_pos[0], peca_pos[1]-1)

            if not posicao_valida(proxima_pos):
                return

            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)

        def direita():
            pos_atual = peca_pos
            proxima_pos = (peca_pos[0], peca_pos[1]+1)

            if not posicao_valida(proxima_pos):
                return

            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)

        def cima_esquerda():
            pos_atual = peca_pos
            proxima_pos = (peca_pos[0]-1, peca_pos[1]-1)
            print(f"{pos_atual} -> {proxima_pos}")

            if not posicao_valida(proxima_pos):
                return

            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)

        def cima_direita():
            pos_atual = peca_pos
            proxima_pos = (peca_pos[0]-1, peca_pos[1])

            if not posicao_valida(proxima_pos):
                return

            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)

        def baixo_direita():
            pos_atual = peca_pos
            proxima_pos = (peca_pos[0]+1, peca_pos[1]+1)

            if not posicao_valida(proxima_pos):
                return

            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)

        def baixo_esquerda():
            pos_atual = peca_pos
            proxima_pos = (peca_pos[0]+1, peca_pos[1])
            
            if not posicao_valida(proxima_pos):
                return

            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)

        #####################
        ### IMPLEMENTAÇÃO ###
        #####################

        movimentos = {
            "e": esquerda,
            "d": direita,
            "ce": cima_esquerda,
            "cd": cima_direita,
            "be": baixo_esquerda,
            "bd": baixo_direita
        }
        
        movimentos[direcao.lower()]()

    def empurrar_oponente(self):
        #Implementar função
        pass

    def checar_vitoria(self):
        return self.pecas_derrubadas[1] >= 6 or self.pecas_derrubadas[2]>=6

    def imprimir_tabuleiro(self):
        tamanho_maximo = len(max(self.tabuleiro, key=len))
        str_final = ""
        str_final += f" \t{" ".join(str(i) for i in range(tamanho_maximo))}\n"
        str_final += "\n"
        for i, linha in enumerate(self.tabuleiro):
            linha_limpa = [x for x in linha if x != -1]
            quantidade_espaços = tamanho_maximo - len(linha_limpa)
            str_final += f"{i}\t"
            str_final += "".join(" " for _ in range(quantidade_espaços))
            str_final += " ".join([str(i) for i in linha_limpa])
            str_final += "\n"
        print(str_final)

    def jogar(self):
        # O usuário vai inserir as coordenadas da peça. ("Linha, Coluna") Ex: 0, 3
        # Temos que pegar a diferença entre a lista com maior tamanho e a lista que ele escolheu
        self.imprimir_tabuleiro()
        print(f"Turno do jogador {self.turno_jogador}")

        # Alterna o turno
        self.turno_jogador = 3 - self.turno_jogador
