from classes.qlearning import Qlearning
from classes.abalone.ambiente import AbaloneAmbiente
from classes.abalone.jogo import JogoAbalone
from classes.abalone.jogador import JogadorAbaloneAgente

if __name__ == "__main__":
    jogo = JogoAbalone()
    jogador_agente = JogadorAbaloneAgente(2)
    ambiente = AbaloneAmbiente(jogo, 1, jogador_agente)
    print(ambiente)
    q_learning = Qlearning(ambiente)

    print("Treinando ambiente...")

    Q, PI = q_learning.calcular_tabela_q()

    print("\nImprimindo Valores por estado:")
    print(ambiente.imprimir_q(Q))
    print("\nImprimindo Polítca ótima por estado:")
    print(ambiente.imprimir_politica(PI))
