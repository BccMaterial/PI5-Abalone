import math
from copy import deepcopy, copy
from classes.abalone.jogada import JogadaAbalone
from classes.base.jogo import Jogo
import random

class JogoAbalone(Jogo):
    def __init__(self, estado = None, turno = 1, placar = None):
        self.estado = estado
        self.placar = placar
        self.ultima_jogada = None
        self._turno = turno
        self.direcoes_possiveis = ["e", "d", "ce", "cd", "be", "bd"]

        if estado is None:
            self.estado = self.criar_tabuleiro()

        if placar is None:
            self.placar = {
                1: 0,
                2: 0
            }

    def turno(self):
        return self._turno

    def proximo_turno(self):
        return 3 - self._turno

    # 1 e 2 são utilizados para representar os espaços ocupados pelas peças 
    # dos jogadores e 0 é utilizado para representar os espaços não ocupados
    def criar_tabuleiro(self):
        """
            Baseado em relação a este tabuleiro: https://www.divertivida.com.br/abalone-classic
            Representação do tabuleiro:
            ```
                2 2 2 2 2
               2 2 2 2 2 2
              - - 2 2 2 - -
             - - - - - - - -
            - - - - - - - - -
             - - - - - - - -
              - - 1 1 1 - - 
               1 1 1 1 1 1
                1 1 1 1 1
            ```
            
            O -1 é pra compensar os tamanhos das listas (vai facilitar na hora de mover)
        """
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

    def movimentar_peca(self, peca_pos: tuple, direcao: str):
        """
        Observações:
        - peca_pos é formada por: (linha, coluna)

        Retorna:
        - 1 se a posição for inválida
        - 0 se for válida
        """
        pos_atual = peca_pos
        pos_atual_valor = self.get_estado(pos_atual)
        proximas_posicoes = [pos_atual]
        proxima_pos = self.calcular_pos(pos_atual, direcao)

        if proxima_pos is None:
            # print("Posição selecionada inválida!")
            return 1

        it_proxima_pos = pos_atual

        # Itera até achar um 0 ou até a borda do tabuleiro
        while it_proxima_pos is not None:
            it_proxima_pos = self.calcular_pos(it_proxima_pos, direcao)

            if self.get_estado(it_proxima_pos) is None:
                break

            if self.get_estado(it_proxima_pos) == 0:
                proximas_posicoes.append(it_proxima_pos)
                break

            if it_proxima_pos is not None:
                proximas_posicoes.append(it_proxima_pos)
        
        # Se todos são iguais, então é uma jogada inválida
        if all(self.get_estado(pos) == pos_atual_valor for pos in proximas_posicoes):
            return 1

        # A primeira posição é 0, então pode mover
        if len(proximas_posicoes) == 1:
            self.set_estado(proxima_pos, self.get_estado(pos_atual))
            self.set_estado(pos_atual, 0)
            self.ultima_jogada = JogadaAbalone(pos_atual, direcao, self.get_estado(pos_atual))
            return 0

        # Handling de quando a primeira posição não é 0
        proximas_posicoes_valores = [self.get_estado(x) for x in proximas_posicoes]

        # Peças seguidas de cada jogador
        j1_pecas_seguidas = 0
        j2_pecas_seguidas = 0

        # Posição da primeira peça de cada jogador na direção
        j1_primeiro_indice = proximas_posicoes_valores.index(1) if 1 in proximas_posicoes_valores else None
        j2_primeiro_indice = proximas_posicoes_valores.index(2) if 2 in proximas_posicoes_valores else None

        # Contagem de peças seguidas
        if j1_primeiro_indice is not None:
            for i in range(j1_primeiro_indice, len(proximas_posicoes)):
                if self.get_estado(proximas_posicoes[i]) != 1:
                    break
                j1_pecas_seguidas += 1

        if j2_primeiro_indice is not None:
            for i in range(j2_primeiro_indice, len(proximas_posicoes)):
                if self.get_estado(proximas_posicoes[i]) != 2:
                    break
                j2_pecas_seguidas += 1

        # Não tem 1, basta só ver se dá pra empurrar os próximos números
        # O número de peças seguidas está como 1 e 2 por que a
        # primeira peça está sendo contada
        if j1_primeiro_indice is None and j2_pecas_seguidas >= 1 and 0 in proximas_posicoes_valores and pos_atual_valor == 2:
            if j2_pecas_seguidas > 3:
                return 1
            # Move as peças encontradas
            i = j2_pecas_seguidas
            while i > j2_primeiro_indice:
                i_pos = proximas_posicoes[i-1]
                i_prox_pos = proximas_posicoes[i]
                self.set_estado((i_prox_pos), self.get_estado(i_pos))
                self.set_estado((i_pos), 0)
                i -= 1
            self.ultima_jogada = JogadaAbalone(pos_atual, direcao, self.get_estado(pos_atual))
            return 0

        # Não tem 2, basta só ver se dá pra empurrar os próximos números
        # O número de peças seguidas está como 1 e 2 por que a
        # primeira peça está sendo contada
        if j2_primeiro_indice is None and j1_pecas_seguidas >= 1 and 0 in proximas_posicoes_valores and pos_atual_valor == 1:
            if j1_pecas_seguidas > 3:
                return 1
            # Move as peças encontradas
            i = j1_pecas_seguidas
            while i > j1_primeiro_indice:
                i_pos = proximas_posicoes[i-1]
                i_prox_pos = proximas_posicoes[i]
                self.set_estado((i_prox_pos), self.get_estado(i_pos))
                self.set_estado((i_pos), 0)
                i -= 1
            # Move a peça que foi selecionada
            self.ultima_jogada = JogadaAbalone(pos_atual, direcao, self.get_estado(pos_atual))
            return 0

        # Ação caso haja peças 1 e 2 na mesma direção
        if j2_primeiro_indice is not None and j1_primeiro_indice is not None:
            diferenca_pecas = 0
            pecas_seguidas_oposto = 0
            if pos_atual_valor == 1:
                diferenca_pecas = j1_pecas_seguidas - j2_pecas_seguidas
                pecas_seguidas_oposto = j2_pecas_seguidas
            elif pos_atual_valor == 2:
                diferenca_pecas = j2_pecas_seguidas - j1_pecas_seguidas
                pecas_seguidas_oposto = j1_pecas_seguidas
            
            # Se for 0 ou menor, não faz nada (Podemos considerar o movimento como inválido)
            if diferenca_pecas <= 0 or pecas_seguidas_oposto >= 3:
                return 1
            else:
                # Caso contrário, empurramos movendo as posições de cada
                # peça, e retirando a última
                i = len(proximas_posicoes) - 1
                self.set_estado(proximas_posicoes[-1], 0)
                while i > 0:
                    i_pos = proximas_posicoes[i-1]
                    i_prox_pos = proximas_posicoes[i]
                    self.set_estado((i_prox_pos), self.get_estado(i_pos))
                    self.set_estado((i_pos), 0)
                    i -= 1
                self.placar[self.turno()] += 1

        self.ultima_jogada = JogadaAbalone(pos_atual, direcao, self.get_estado(pos_atual))
        return 0

    def posicao_valida(self, pos: tuple):
        linha = pos[0]
        coluna = pos[1]

        if linha < 0 or linha >= len(self.estado):
            return False

        if coluna < 0 or coluna >= len(self.estado[linha]):
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
        proxima_pos = movimentos.get(direcao, None)

        if proxima_pos is None or proxima_pos[0] not in range(0, len(self.estado)):
            return None

        prox_linha = proxima_pos[0]
        prox_linha_len = len(self.estado[prox_linha])
        linha_atual_len = len(self.estado[pos[0]])
        diff_len = linha_atual_len - prox_linha_len
        if diff_len >= 1:
            diff_len -= 1
        proxima_pos = (proxima_pos[0], proxima_pos[1] - diff_len)

        if not self.posicao_valida(proxima_pos):
            return None

        return proxima_pos

    def set_estado(self, pos: tuple, valor: int):
        linha, coluna = pos
        self.estado[linha][coluna] = valor

    def get_estado(self, pos: tuple):
        if pos is None:
            return None
        linha, coluna = pos
        return self.estado[linha][coluna]

    def jogar(self, jogada: JogadaAbalone):
        temp = deepcopy(self)
        temp.movimentar_peca(jogada.posicao, jogada.direcao)
        return JogoAbalone(temp.estado, temp.proximo_turno(), temp.placar)

    def jogadas_validas(self):
        lista_jogadas = []
        for i in range(len(self.estado)):
            for j in range(len(self.estado[i])):
                pos = (i, j)
                if self.get_estado(pos) != self.turno():
                    continue
                for direcao in self.direcoes_possiveis:
                    jogo_copy = deepcopy(self)
                    resultado_movimento = jogo_copy.movimentar_peca(pos, direcao)
                    if self.calcular_pos(pos, direcao) is not None and resultado_movimento != 1:
                        lista_jogadas.append(JogadaAbalone(pos, direcao, self.turno()))
        return lista_jogadas

    def venceu(self):
        return self.placar[self.turno()] >= 6

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

    def calcular_utilidade(self, jogador):
        # Constantes de peso para cada fator
        PESO_CENTRO = 3.0
        PESO_AGRUPAMENTO = 1.5
        PESO_EMPURRAR = 2.0
        PESO_RISCO = 0.1
        PESO_PECAS = 1.0
        
        util_total = 0
        num_pecas_jogador = 0
        num_pecas_oponente = 0
        pecas_empurraveis = 0
        pecas_em_risco = 0
        
        centro = (4, 4)  # Posição central
        
        for i in range(len(self.estado)):
            for j in range(len(self.estado[i])):
                pos = (i, j)
                if self.get_estado(pos) == 3 - jogador:
                    num_pecas_oponente += 1
                    continue
                if self.get_estado(pos) != jogador:
                    continue
                    
                num_pecas_jogador += 1
                
                # 1. Avaliação de empurrão/risco
                pode_empurrar = False
                em_risco = False
                
                for direcao in self.direcoes_possiveis:
                    linha = self.verificar_linha(pos, direcao)
                    if not linha:
                        continue
                        
                    if self.quem_pode_empurrar([self.get_estado(pos)] + linha) == jogador:
                        pode_empurrar = True
                    elif self.quem_pode_empurrar([self.get_estado(pos)] + linha) == 3 - jogador:
                        em_risco = True
                
                if pode_empurrar:
                    pecas_empurraveis += 1
                if em_risco:
                    pecas_em_risco += 1
                
                # 2. Distância ao centro (usando distância de Manhattan)
                distancia_centro = abs(pos[0] - centro[0]) + abs(pos[1] - centro[1])
                valor_centro = 1 / (1 + distancia_centro)  # Valor entre 0 e 1
                
                # 3. Avaliação de agrupamento
                vizinhos_aliados = 0
                for direcao in self.direcoes_possiveis:
                    vizinho = self.calcular_pos(pos, direcao)
                    if vizinho and self.get_estado(vizinho) == jogador:
                        vizinhos_aliados += 1
                
                # 4. Contribuição para a utilidade total
                # if not (pode_empurrar or em_risco):  # Só considera se não estiver em situação crítica
                util_total += (valor_centro * PESO_CENTRO + 
                              (vizinhos_aliados/6) * PESO_AGRUPAMENTO)
        
        # Fatores globais
        diferenca_pecas = (14 - num_pecas_jogador) - (14 - (sum(sum(1 for x in linha if x == (3 - jogador)) for linha in self.estado)))

        # Utilidade final combinando todos os fatores
        utilidade = (
            (util_total / max(1, num_pecas_jogador)) +  # Média da utilidade posicional
            pecas_empurraveis * PESO_EMPURRAR +
            pecas_em_risco * PESO_RISCO +
            diferenca_pecas * PESO_PECAS
        )
        return utilidade

    def verificar_linha(self, pos, direcao):
        """Retorna os valores na direção especificada até encontrar um 0 ou None"""
        valores = []
        prox_pos = self.calcular_pos(pos, direcao)
        
        while prox_pos is not None and self.get_estado(prox_pos) != 0:
            valores.append(self.get_estado(prox_pos))
            prox_pos = self.calcular_pos(prox_pos, direcao)
        
        return valores

    # def pos_utilidade(self, pos: tuple):
    #     pecas_direcoes = dict()
    #     pos_valor = self.get_estado(pos)
    #     # Armazena os valores de cada direção
    #
    #     for direcao in self.direcoes_possiveis:
    #         pecas_direcoes[direcao] = list()
    #         proximo_valor = -1
    #         proxima_pos = pos
    #         # Itera nas casas até achar 0 ou até a borda
    #         while proximo_valor != 0 and proximo_valor != None:
    #             proxima_pos = self.calcular_pos(proxima_pos, direcao)
    #             proximo_valor = self.get_estado(proxima_pos)
    #             if proximo_valor is not None:
    #                 pecas_direcoes[direcao].append(proximo_valor)
    #
    #     # Valida se pode ser empurrado em qualquer direção
    #     # Se em qualquer direção pode ser empurrado, retorna 1.
    #     # Se em qualquer direção pode empurrar, retorna 0
    #     for direcao in self.direcoes_possiveis:
    #         lista_valores = pecas_direcoes[direcao]
    #
    #         # Se tiver 0, pula, pois não pode empurrar ou ser empurrado
    #         if 0 in lista_valores:
    #             continue
    #
    #         if self.quem_pode_empurrar([pos_valor, *lista_valores]) == pos_valor:
    #             return float("-inf")
    #         else:
    #             return float("+inf")
    #
    # def calcular_utilidade(self, jogador):
    #     util_total = 0 #Soma das utilidades de todas as peças do jogador
    #     num_pecas_jogador = 0
    #     pecas_empurraveis = 0
    #     pecas_em_risco = 0 #Quantidade de peças do jogador que podem ser empurradas
    #
    #     for i in range(len(self.estado)): #Linha
    #         for j in range(len(self.estado[i])): #Coluna
    #             posicao = (i, j)
    #
    #             if self.get_estado(posicao) != jogador: #Verifica se a peça não pertence ao jogador
    #                 continue
    #
    #             val_utilidade = self.pos_utilidade(posicao)
    #
    #             if val_utilidade == float('inf'): #Se retorna inf, pode empurrar
    #                 pecas_empurraveis += 1
    #             elif val_utilidade == float('-inf'): #Se retorna inf, pode ser empurrada
    #                 pecas_em_risco += 1
    #             else: #Caso não possa empurrar ou ser empurrada, calcula a distância até o centro
    #                 util_total += val_utilidade
    #
    #             num_pecas_jogador += 1
    #
    #     if num_pecas_jogador == 0:
    #         return 0
    #
    #     utilidade_media = util_total / num_pecas_jogador
    #
    #     return utilidade_media + (2 * pecas_empurraveis) - (1.5 * pecas_em_risco) #Cada peça que pode empurrar ganha um bônus de +2 e cada peça que pode ser empurrada sobre uma penalização de -1.5

    def imprimir_jogada(self, jogador, jogada: JogadaAbalone):
        print(f"Jogador {jogador.identificador} moveu a peça {jogada.posicao} na direção {jogada.direcao}")

    def imprimir(self):
        tamanho_maximo = len(max(self.estado, key=len))
        str_final = ""
        str_final += f" \t{' '.join(str(i) for i in range(tamanho_maximo))}\n"
        str_final += "\n"
        for i, linha in enumerate(self.estado):
            quantidade_espaços = tamanho_maximo - len(linha)
            str_final += f"{i}\t"
            str_final += "".join(" " for _ in range(quantidade_espaços))
            str_final += " ".join([str(i) for i in linha])
            str_final += "\n"
        str_final += "\nPlacar:\n"
        str_final += f"Jogador 1: {self.placar[1]}\n"
        str_final += f"Jogador 2: {self.placar[2]}\n"
        print(str_final)
