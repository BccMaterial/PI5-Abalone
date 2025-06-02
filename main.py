import time
from classes.abalone.jogo import JogoAbalone
from classes.abalone.jogador import JogadorAbaloneHumano, JogadorAbaloneAgente

if __name__ == "__main__":
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

