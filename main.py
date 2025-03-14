from classes import Abalone

if __name__ =="__main__":
    jogo = Abalone() #Cria um jogo
    jogo.imprimir_tabuleiro()
    jogo.movimentar_peca((6, 4), "ce")
    jogo.imprimir_tabuleiro()
    jogo.movimentar_peca((5, 3), "bd")
    jogo.imprimir_tabuleiro()
