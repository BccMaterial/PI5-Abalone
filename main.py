import time
from classes.abalone.jogo import JogoAbalone
from classes.abalone.jogador import JogadorAbaloneHumano, JogadorAbaloneAgente
from classes.qlearning import JogadorQLearning, treinar_qlearning
import os

def jogador_vs_minimax():
    jogador_humano = JogadorAbaloneHumano(1)
    jogador_agente = JogadorAbaloneAgente(2)
    jogo = JogoAbalone(turno=jogador_humano.identificador)

    while True:
        # Turno do jogador
        if isinstance(jogador_humano, JogadorAbaloneAgente):
            print(f"Jogador {jogador_humano.imprimir()} está pensando...")
            time.sleep(1.5)

        jogada_humano = jogador_humano.jogar(jogo)
        print("==================================================")
        jogo.imprimir_jogada(jogador_humano, jogada_humano)
        jogo = jogo.jogar(jogada_humano)

        if jogo.venceu():
            print(f"{jogador_humano.imprimir()} venceu!")
            break

        # Turno do agente
        print("Situação do jogo:")
        jogo.imprimir()
        print("==================================================")

        if isinstance(jogador_agente, JogadorAbaloneAgente):
            print(f"Jogador {jogador_agente.imprimir()} está pensando...")
            time.sleep(1.5)

        jogada_agente = jogador_agente.jogar(jogo)
        jogo.imprimir_jogada(jogador_agente, jogada_agente)
        print("==================================================")
        jogo = jogo.jogar(jogada_agente)

        if jogo.venceu():
            print(f"{jogador_agente.imprimir()} venceu!")
            break

def jogador_vs_qlearning():
    jogador_humano = JogadorAbaloneHumano(2)
    jogador_agente = JogadorQLearning(1)
    jogo = JogoAbalone(turno=jogador_humano.identificador)

    while True:
        # Turno do jogador
        if isinstance(jogador_humano, JogadorAbaloneAgente):
            print(f"Jogador {jogador_humano.imprimir()} está pensando...")
            time.sleep(1.5)

        jogada_humano = jogador_humano.jogar(jogo)
        print("==================================================")
        jogo.imprimir_jogada(jogador_humano, jogada_humano)
        jogo = jogo.jogar(jogada_humano)

        if jogo.venceu():
            print(f"{jogador_humano.imprimir()} venceu!")
            break

        # Turno do agente
        print("Situação do jogo:")
        jogo.imprimir()
        print("==================================================")

        if isinstance(jogador_agente, JogadorAbaloneAgente):
            print(f"Jogador {jogador_agente.imprimir()} está pensando...")
            time.sleep(1.5)

        jogada_agente = jogador_agente.jogar(jogo)
        jogo.imprimir_jogada(jogador_agente, jogada_agente)
        print("==================================================")
        jogo = jogo.jogar(jogada_agente)

        if jogo.venceu():
            print(f"{jogador_agente.imprimir()} venceu!")
            break

def minimax_vs_qlearning():
    jogador_qlearning = JogadorQLearning(1)
    jogador_minimax = JogadorAbaloneAgente(2)
    jogo = JogoAbalone(turno=jogador_qlearning.identificador)

    while True:
        # Turno do jogador
        print(f"Jogador {jogador_qlearning.imprimir()} está pensando...")
        time.sleep(1.5)

        jogada_qlearning = jogador_qlearning.jogar(jogo)
        print("==================================================")
        jogo.imprimir_jogada(jogador_qlearning, jogada_qlearning)
        jogo = jogo.jogar(jogada_qlearning)

        if jogo.venceu():
            print(f"{jogador_qlearning.imprimir()} venceu!")
            break

        # Turno do agente
        print("Situação do jogo:")
        jogo.imprimir()
        print("==================================================")

        print(f"Jogador {jogador_minimax.imprimir()} está pensando...")
        time.sleep(1.5)

        jogada_minimax = jogador_minimax.jogar(jogo)
        jogo.imprimir_jogada(jogador_minimax, jogada_minimax)
        print("==================================================")
        jogo = jogo.jogar(jogada_minimax)

        if jogo.venceu():
            print(f"{jogador_minimax.imprimir()} venceu!")
            break

def jogador_vs_jogador():
    jogador_1 = JogadorAbaloneHumano(1)
    jogador_2 = JogadorAbaloneHumano(2)
    jogo = JogoAbalone(turno=jogador_1.identificador)

    while True:
        # Turno jogador 1
        jogada_1 = jogador_1.jogar(jogo)
        print("==================================================")
        jogo.imprimir_jogada(jogador_1, jogada_1)
        jogo = jogo.jogar(jogada_1)

        if jogo.venceu():
            print(f"{jogador_1.imprimir()} venceu!")
            break

        # Turno jogador 2
        print("Situação do jogo:")
        jogo.imprimir()
        print("==================================================")

        jogada_2 = jogador_2.jogar(jogo)
        jogo.imprimir_jogada(jogador_2, jogada_2)
        print("==================================================")
        jogo = jogo.jogar(jogada_2)

        if jogo.venceu():
            print(f"{jogador_2.imprimir()} venceu!")
            break

if __name__ == "__main__":
    user_input = 0
    while True:
        os.system("cls||clear")
        print("ABALONE")
        print("==================================================")
        print("1 - Jogador vs. Jogador")
        print("2 - Jogador vs. Minimax")
        print("3 - Jogador vs. Q-Learning")
        print("4 - Q-Learning vs. Minimax")
        print("5 - Treinar Q-Learning (1 Partida)")
        print("6 - Sair")
        user_input_str = input("Insira um comando: ")
        if not user_input_str.isdigit():
            print("ERRO: Insira um valor válido!")
            time.sleep(3)
            continue

        user_input = int(user_input_str)

        match user_input:
            case 1:
                jogador_vs_jogador()
            case 2:
                jogador_vs_minimax()
            case 3:
                jogador_vs_qlearning()
            case 4:
                minimax_vs_qlearning()
            case 5:
                treinar_qlearning(num_episodios=1, salvar_cada=1)
            case 6:
                break
            case _:
                print("ERRO: Insira um valor válido!")
                time.sleep(3)
                continue

