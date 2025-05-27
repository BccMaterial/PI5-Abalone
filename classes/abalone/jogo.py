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
        j1_primeiro_indice = valores.index(1) if 1 in valores else None
        j2_primeiro_indice = valores.index(2) if 2 in valores else None


        if j1_primeiro_indice is None or j2_primeiro_indice is None:
            return 0

        j1_pecas_seguidas = 0
        for i in range(j1_primeiro_indice, len(valores)):
            if valores[i] != 1:
                break
            j1_pecas_seguidas += 1

        j2_pecas_seguidas = 0
        for i in range(j2_primeiro_indice, len(valores)):
            if valores[i] != 2:
                break
            j2_pecas_seguidas += 1

        if j1_primeiro_indice < j2_primeiro_indice and j1_pecas_seguidas > j2_pecas_seguidas:
            return 1
        else:
            return 2

    def calcular_utilidade(self, jogador):
        qtd_pecas = 0
        total_pecas = 0
        tabuleiro = self.estado
        x_c, y_c = 4, 4
        total_coef_centro = 0
        for x in range(len(tabuleiro)):
            for y in range(len(tabuleiro[x])):
                peca = tabuleiro[x][y]
                total_pecas += 1 if peca != 0 else 0
                if peca == jogador:
                    qtd_pecas += 1
                    peca_distancia_centro = abs(x - x_c) + abs(y - y_c)
                    coef_centro = 1 / max(1, peca_distancia_centro)
                    total_coef_centro += coef_centro
        
        utilidade = total_coef_centro + (qtd_pecas/total_pecas)
        return utilidade
    
    def verificar_linha(self, pos, direcao):
        """
            Retorna os valores na direção especificada até encontrar um 0 ou None
        """
        valores = []
        prox_pos = self.calcular_pos(pos, direcao)
        
        while prox_pos is not None and self.get_estado(prox_pos) != 0:
            valores.append(self.get_estado(prox_pos))
            prox_pos = self.calcular_pos(prox_pos, direcao)
        
        return valores

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
