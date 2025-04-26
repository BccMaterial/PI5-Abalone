from classes.base.jogador import JogadorAgente, JogadorHumano
from classes.abalone.jogada import JogadaAbalone
import re

class JogadorAbaloneHumano(JogadorHumano):
    def jogar(self, jogo):
        jogada = JogadaAbalone((-1, -1), "")
        jogo.imprimir()
        print("Instruções")
        print("----------------------------------")
        print("- Insira a coordenada da peça que você deseja mover -> \"NLinha, NColuna\"")
        print("- Você pode contar as linhas a partir do 0")
        print("- Caso queira sair, digite q")
        print(f"Turno do jogador {self.identificador}")
        while not jogada.e_valida(jogo):
            ultimo_input = input("Digite as coordenadas \"NLinha, NColuna\": ")
            if ultimo_input == "q":
                print("Encerrando processo...")
                exit(0)

            if not re.match(r"^\d,\s?\d$", ultimo_input):
                print("Formato inválido. Por favor, digite no formato \"NLinha, NColuna\"")
                continue
            
            pos_inserida = tuple([int(x) for x in re.split(r",\s?", ultimo_input)])
            jogada.posicao = pos_inserida

            if jogo.get_estado(pos_inserida) != jogo.turno():
                print("A peça selecionada é do outro jogador! Por favor, selecione outra.")
                continue

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

                if len([x for x in jogo.direcoes_possiveis if x == ultimo_input]) < 1:
                    print("Direção inválida! Por favor, digite uma direção válida.")
                    continue

                if ultimo_input == "q":
                    return

                jogada.direcao = ultimo_input
                direcao_valida = True
            if not jogada.e_valida(jogo):
                print(f"Jogada inválida! Selecione as suas peças, ou mova para uma direção válida.")
        return jogada

class JogadorAbaloneAgente(JogadorAgente):
    def __init__(self, identificador):
        super().__init__(identificador)
