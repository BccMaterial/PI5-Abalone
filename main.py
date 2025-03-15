from classes import Abalone

if __name__ =="__main__":
    jogo = Abalone() # Cria um jogo
    jogo.imprimir_tabuleiro()
    jogo.movimentar_peca((6, 2), "cd")
    jogo.imprimir_tabuleiro()
    jogo.movimentar_peca((5, 3), "cd")
    jogo.imprimir_tabuleiro()
    jogo.movimentar_peca((4, 4), "cd")
    jogo.imprimir_tabuleiro()
