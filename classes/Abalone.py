import math
import re, random
from .no import No
from copy import deepcopy
from math import sqrt

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
            [0, 0, 0, 0, 0, 0, 0, 0, 0], #Centro: (4,4)
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 0],
            [2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2,],
        ]

    def gerar_sucessores(self, no: No):
        estado = deepcopy(no.estado)
        possiveis_direcoes = ["e", "d", "ce", "cd", "be", "bd"]
        nos_sucessores = []

        random.shuffle(possiveis_direcoes)
        for i, linha in enumerate(self.tabuleiro):
            for j, coluna in enumerate(linha):
                if coluna == 0:
                    continue
                for direcao in possiveis_direcoes:
                    tupla = (i, j)
                    coef_util = self.funcao_utilidade(tupla)
                    distancia_centro = self.calc_distancia_centro(tupla)
                    tabuleiro_original = deepcopy(self.tabuleiro)
                    tabuleiro_original.movimentar_peca(tupla, direcao)

                    if estado != self.tabuleiro:
                        nos_sucessores.append(No(tabuleiro_original.tabuleiro, no, f"{tupla} {direcao}", coef_util, distancia_centro))

                    self.tabuleiro = tabuleiro_original

        return nos_sucessores

    def funcao_utilidade(self, pos: tuple):
        direcoes = ["e", "d", "ce", "cd", "be", "bd"]
        pecas_direcoes = dict()
        pos_valor = self.get_tabuleiro(pos)

        for direcao in direcoes:
            pecas_direcoes[direcao] = list()
            proximo_valor = -1
            proxima_pos = pos
            # Itera nas casas até achar 0 ou até a borda
            while proximo_valor != 0 and proximo_valor != None:
                proxima_pos = self.calcular_pos(proxima_pos, direcao)
                proximo_valor = self.get_tabuleiro(proxima_pos)
                if proximo_valor is not None:
                    pecas_direcoes[direcao].append(proximo_valor)

        # Se em qualquer direção pode ser empurrado, retorna 1.
        # Se em qualquer direção pode empurrar, retorna 0
        for direcao in direcoes:
            lista_valores = pecas_direcoes[direcao]

            if 0 in lista_valores:
                continue

            if self.quem_pode_empurrar([pos_valor, *lista_valores]) == pos_valor:
                return 0
            else:
                return 1

        # Caso não possa empurrar ou ser empurrado, calcula o coef_utilidade até o centro
        posicoes_ao_redor = [self.calcular_pos(pos, x) for x in direcoes]
        posicoes_ao_redor_valores = [self.get_tabuleiro(pos) for pos in posicoes_ao_redor]
        qtd_pecas_ao_redor = len([x for x in posicoes_ao_redor_valores if x != 0])
        distancia_centro = self.calc_distancia_centro(pos)
        coef_utilidade = qtd_pecas_ao_redor/(distancia_centro+1)
        return coef_utilidade

    def quem_pode_empurrar(self, valores):
        """
        Dado um array de valores de 1 e 2, verifica quem pode empurrar naquela situação

        0 -> nenhuma peça pode ser empurrada
        1 -> jogador 1 pode empurrar
        2 -> jogador 2 pode empurrar
        """
        qtd_pecas_j1 = len([x for x in valores if x == 1])
        qtd_pecas_j2 = len([x for x in valores if x == 2])
        
        if qtd_pecas_j1 == qtd_pecas_j2 or 0 in valores:
            return 0

        if qtd_pecas_j1 == 0 or qtd_pecas_j2 == 2:
            return 0

        qtd_pecas_j1_primeiro_indice = valores.index(1)
        qtd_pecas_j2_primeiro_indice = valores.index(2)
        
        if qtd_pecas_j1 > qtd_pecas_j2 and qtd_pecas_j1_primeiro_indice < qtd_pecas_j2_primeiro_indice:
            return 1
        else:
            return 2


    # Get e set compatível com tuplas
    def get_tabuleiro(self, pos: tuple):
        if pos is None:
            return None
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
        pos_atual_valor = self.get_tabuleiro(pos_atual)
        proximas_posicoes = []
        proxima_pos = self.calcular_pos(pos_atual, direcao)

        if proxima_pos is None:
            # print("Posição selecionada inválida!")
            return

        it_proxima_pos = pos_atual

        # Itera até achar um 0 ou até a última posição da direção
        while it_proxima_pos is not None:
            it_proxima_pos = self.calcular_pos(it_proxima_pos, direcao)
            if self.get_tabuleiro(it_proxima_pos) is None:
                break

            if self.get_tabuleiro(it_proxima_pos) == 0:
                proximas_posicoes.append(it_proxima_pos)
                break

            if it_proxima_pos is not None:
                proximas_posicoes.append(it_proxima_pos)


        # A primeira posição é 0
        if len(proximas_posicoes) == 1:
            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)
            return 0

        # Handling de quando a primeira posição não é 0
        proximas_posicoes_valores = [self.get_tabuleiro(x) for x in proximas_posicoes]

        # Peças seguidas de cada jogador
        j1_pecas_seguidas = 0
        j2_pecas_seguidas = 0

        # Posição da primeira peça de cada jogador na direção
        j1_primeiro_indice = proximas_posicoes_valores.index(1) if 1 in proximas_posicoes_valores else None
        j2_primeiro_indice = proximas_posicoes_valores.index(2) if 2 in proximas_posicoes_valores else None

        # Contagem de peças seguidas
        for posicao in proximas_posicoes:
            if self.get_tabuleiro(posicao) != 1:
                continue
            j1_pecas_seguidas += 1

        for posicao in proximas_posicoes:
            if self.get_tabuleiro(posicao) != 2:
                continue
            j2_pecas_seguidas += 1

        # Não tem 1, basta só ver se dá pra empurrar os próximos números
        if j1_primeiro_indice is None and j2_pecas_seguidas in [1, 2] and 0 in proximas_posicoes_valores:
            # Move as peças encontradas
            i = j2_pecas_seguidas
            while i > j2_primeiro_indice:
                i_pos = proximas_posicoes[i-1]
                i_prox_pos = proximas_posicoes[i]
                self.set_tabuleiro((i_prox_pos), self.get_tabuleiro(i_pos))
                self.set_tabuleiro((i_pos), 0)
                i -= 1
            # Move a peça que foi selecionada
            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)
            return 0

        # Não tem 1, basta só ver se dá pra empurrar os próximos números
        # O número de peças seguidas está como 1 e 2 por que a
        # primeira peça está sendo contada
        if j2_primeiro_indice is None and j1_pecas_seguidas in [1, 2] and 0 in proximas_posicoes_valores:
            # Move as peças encontradas
            i = j1_pecas_seguidas
            while i > j1_primeiro_indice:
                i_pos = proximas_posicoes[i-1]
                i_prox_pos = proximas_posicoes[i]
                self.set_tabuleiro((i_prox_pos), self.get_tabuleiro(i_pos))
                self.set_tabuleiro((i_pos), 0)
                i -= 1
            # Move a peça que foi selecionada
            self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
            self.set_tabuleiro(pos_atual, 0)
            return 0

        # Ação caso haja peças 1 e 2 na mesma direção
        if j2_primeiro_indice is not None and j1_primeiro_indice is not None:
            # É adicionado +1 dependendo do valor da posição atual
            diferenca_pecas = 0
            if pos_atual_valor == 1:
                diferenca_pecas = (j1_pecas_seguidas + 1) - j2_pecas_seguidas
            elif pos_atual_valor == 2:
                diferenca_pecas = (j2_pecas_seguidas + 1) - j1_pecas_seguidas
            
            # Se for 0 ou menor, não faz nada (Podemos considerar o movimento como inválido)
            if diferenca_pecas <= 0 and abs(diferenca_pecas) >= 3:
                return 1
            else:
                i = len(proximas_posicoes) - 1
                self.retirar_peca(proximas_posicoes[-1])
                while i > 0:
                    i_pos = proximas_posicoes[i-1]
                    i_prox_pos = proximas_posicoes[i]
                    self.set_tabuleiro((i_prox_pos), self.get_tabuleiro(i_pos))
                    self.set_tabuleiro((i_pos), 0)
                    i -= 1
                self.set_tabuleiro(proxima_pos, self.get_tabuleiro(pos_atual))
                self.set_tabuleiro(pos_atual, 0)
                self.pecas_derrubadas[pos_atual_valor] += 1

        return 0

    def posicao_valida(self, pos: tuple):
        linha = pos[0]
        coluna = pos[1]

        if linha < 0 or linha >= len(self.tabuleiro):
            return False

        if coluna < 0 or coluna >= len(self.tabuleiro[linha]):
            return False

        return True

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

        direcao = direcao.lower()
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

    def testar_objetivo(self):
        return self.pecas_derrubadas[1] >= 6 or self.pecas_derrubadas[2] >= 6

    def imprimir_tabuleiro(self):
        tamanho_maximo = len(max(self.tabuleiro, key=len))
        str_final = ""
        str_final += f" \t{' '.join(str(i) for i in range(tamanho_maximo))}\n"
        str_final += "\n"
        for i, linha in enumerate(self.tabuleiro):
            quantidade_espaços = tamanho_maximo - len(linha)
            str_final += f"{i}\t"
            str_final += "".join(" " for _ in range(quantidade_espaços))
            str_final += " ".join([str(i) for i in linha])
            str_final += "\n"
        print(str_final)

    def retirar_peca(self, pos: tuple):
        """
        Summary
            Dada uma posição, retira a peça
        Returns
            Retorna o valor que foi retirado
        """
        valor_retirado = self.get_tabuleiro(pos)
        self.set_tabuleiro(pos, 0)
        return valor_retirado

    def jogar(self):
        # O usuário vai inserir as coordenadas da peça. ("Linha, Coluna") Ex: 0, 3
        # Temos que pegar a diferença entre a lista com maior tamanho e a lista que ele escolheu
        ultimo_input = ""
        while not self.testar_objetivo():
            self.imprimir_tabuleiro()
            print("Instruções")
            print("----------------------------------")
            print("- Insira a coordenada da peça que você deseja mover -> \"NLinha, NColuna\"")
            print("- Você pode contar as linhas a partir do 0")
            print("- Caso queira sair, digite q")
            print(f"Turno do jogador {self.turno_jogador}")

            pos_valida = False
            while not pos_valida:
                ultimo_input = input("Digite as coordenadas (NLinha, NColuna): ")
                if ultimo_input == "q":
                    return

                if not re.match(r"\d,\s\d", ultimo_input):
                    print("Formato inválido. Por favor, digite no formato \"NLinha, NColuna\"")
                    continue
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
            direcao_valida = False
            while not direcao_valida:
                ultimo_input = input("Agora, digite a direção: ")
                direcoes_possiveis = ["e", "d", "ce", "cd", "be", "bd"]
                
                if len([x for x in direcoes_possiveis if x == ultimo_input]) < 1:
                    print("Direção inválida! Por favor, digite uma direção válida.")
                    continue

                if ultimo_input == "q":
                    return

                direcao = ultimo_input
                direcao_valida = True

            self.movimentar_peca(pos_inserida, direcao)

            # Alterna o turno
            self.turno_jogador = 3 - self.turno_jogador

    def distancia_centro(self):
        centro_tabuleiro = (4,4) #Aproximadamente o ponto central do tabuleiro
        distancias_centro = {} #Distancia de cada esfera em relação ao centro
        tabuleiro = self.tabuleiro

        for i, linha in enumerate(tabuleiro): #Percorre as linhas
            for j, esfera in enumerate(linha): #Percorre cada peça dentro das listas
                if esfera in [1,2]:
                    distancia = abs(math.pow((i-centro_tabuleiro[0]), 2) + math.pow((j - centro_tabuleiro[1]), 2)) #Distância de manhattan
                    distancias_centro[(i,j)] = distancia

        return distancias_centro

    def calc_distancia_centro(self, pos: tuple):
        x, y = pos
        c_x, c_y = (4, 4)
        return abs(math.pow((x - c_x), 2) + math.pow((y - c_y), 2))


