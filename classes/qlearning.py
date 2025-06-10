import random
import pickle
from collections import defaultdict
from classes.base.jogador import Jogador
from classes.minimax import minimax_alfabeta
from classes.abalone.jogo import JogoAbalone
import os

class JogadorQLearning(Jogador):
    def __init__(self, identificador, alpha=0.3, gamma=0.85, epsilon=0.18):
        super().__init__(identificador, "max")
        self.q_table = defaultdict(float)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def hash_estado(self, jogo):
        # Hash simples: transforme o estado do tabuleiro em string
        return str(jogo.estado)

    def escolher_acao(self, jogo):
        estado = self.hash_estado(jogo)
        jogadas = jogo.jogadas_validas()
        if not jogadas:
            return None
        # Epsilon-greedy
        if random.random() < self.epsilon:
            return random.choice(jogadas)
        qs = [self.q_table[(estado, str(jogada))] for jogada in jogadas]
        max_q = max(qs)
        melhores = [j for j, q in zip(jogadas, qs) if q == max_q]
        return random.choice(melhores)

    def jogar(self, jogo):
        # Para compatibilidade com a interface Jogador
        return self.escolher_acao(jogo)

    def atualizar_q(self, estado, acao, recompensa, proximo_estado, proxima_acao):
        chave = (estado, str(acao))
        proxima_chave = (proximo_estado, str(proxima_acao))
        q_atual = self.q_table[chave]
        q_proximo = self.q_table[proxima_chave]
        self.q_table[chave] = q_atual + self.alpha * (recompensa + self.gamma * q_proximo - q_atual)

    def salvar_qtable(self, caminho="qtable.pkl"):
        with open(caminho, "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def carregar_qtable(self, caminho="qtable.pkl"):
        with open(caminho, "rb") as f:
            self.q_table = defaultdict(float, pickle.load(f))


def treinar_qlearning(num_episodios=100, salvar_cada=10):
    q_agent = JogadorQLearning(1)
    minimax_id = 2
    q_vitorias = 0
    min_max_vitorias = 0

    for episodio in range(num_episodios):
        jogo = JogoAbalone()
        estado = q_agent.hash_estado(jogo)
        acao = q_agent.escolher_acao(jogo)
        while not jogo.finalizou():
            # Q-Learning joga
            os.system("cls||clear")
            print(f"Executando episódio {episodio} de {num_episodios}...")
            print(jogo)
            print(f"Vitórias (Q-Learning): {q_vitorias} ({(q_vitorias/num_episodios)*100:.2f}%)")
            print(f"Vitórias (MiniMax): {min_max_vitorias} ({(min_max_vitorias/num_episodios)*100:.2f}%)")
            if acao is None:
                break
            placar_anterior = jogo.placar
            jogo_q = jogo.jogar(acao)
            recompensa = jogo_q.calcular_utilidade(q_agent.identificador)

            if jogo_q.placar[q_agent.identificador] > placar_anterior[q_agent.identificador]:
                recompensa += 50

            if jogo_q.placar[minimax_id] > placar_anterior[minimax_id]:
                recompensa -= 50

            if jogo.finalizou():
                if jogo_q.placar[q_agent.identificador] > placar_anterior[q_agent.identificador]:
                    recompensa += 100
                if jogo_q.placar[minimax_id] > placar_anterior[minimax_id]:
                    recompensa -= 100

            print(f"Ultima recompensa: {recompensa}")

            # Minimax joga
            jogadas_minimax = jogo_q.jogadas_validas()
            if not jogadas_minimax:
                break
            melhor_jogada_minimax = None
            melhor_valor = float("-inf")
            for jogada in jogadas_minimax:
                valor = minimax_alfabeta(jogo_q.jogar(jogada), True, minimax_id, profundidade_maxima=2)
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_jogada_minimax = jogada
            jogo_minimax = jogo_q.jogar(melhor_jogada_minimax)

            proximo_estado = q_agent.hash_estado(jogo_minimax)
            proxima_acao = q_agent.escolher_acao(jogo_minimax)
            q_agent.atualizar_q(estado, acao, recompensa, proximo_estado, proxima_acao)

            # Avança para próximo estado
            estado = proximo_estado
            acao = proxima_acao
            jogo = jogo_minimax
        if jogo.placar[q_agent.identificador] >= 6:
            q_vitorias += 1
        if jogo.placar[minimax_id] >= 6:
            min_max_vitorias += 1
        os.system("cls||clear")
        print(f"Executado episódio {episodio+1} de {num_episodios}...")
        print(jogo)
        if (episodio+1) % salvar_cada == 0:
            print(f"Episódio {episodio+1} concluído.")
            q_agent.salvar_qtable("qtable.pkl")
    print("Treinamento concluído!")
    print("Commitando qtable.pkl...")
    commit_changes()

def commit_changes():
    os.system("git add qtable.pkl")
    os.system("git status")
    os.system("git commit -m 'Update Q-Learning table (AUTOMATED COMMIT)'")
    os.system("git push")

if __name__ == "__main__":
    treinar_qlearning(num_episodios=50)
