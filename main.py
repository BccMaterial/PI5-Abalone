import time
from classes.abalone.jogo import JogoAbalone
from classes.abalone.jogador import JogadorAbaloneHumano, JogadorAbaloneAgente

if __name__ == "__main__":
    jogo = JogoAbalone()
    jogador_humano = JogadorAbaloneHumano(1)
    jogador_agente = JogadorAbaloneAgente(2)

    print("Situação do jogo:")
    while True:
        # Turno do jogador
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

        print(f"Jogador {jogador_agente.imprimir()} está pensando...")
        time.sleep(1.5)

        jogada_agente = jogador_agente.jogar(jogo)
        print(jogo.imprimir_jogada(jogador_agente, jogada_agente))
        print("==================================================")
        jogo = jogo.jogar(jogada_agente)

        if jogo.venceu():
            print(f"{jogador_humano.imprimir()} venceu!")
            break

