import math
from copy import deepcopy

# Definição das constantes para jogadores e espaços vazios
X = "X"
O = "O"
EMPTY = None

def initial_state():
    # Inicializa e retorna o estado inicial do tabuleiro
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    # Determina qual jogador tem a próxima jogada em um dado tabuleiro
    Xcount = sum(row.count(X) for row in board)
    Ocount = sum(row.count(O) for row in board)

    return X if Xcount <= Ocount else O

def actions(board):
    # Retorna um conjunto de todas as ações possíveis (i, j) disponíveis no tabuleiro
    return {(i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == EMPTY}

def result(board, action):
    # Retorna o tabuleiro resultante de realizar uma jogada (i, j) no tabuleiro
    if board[action[0]][action[1]] is not EMPTY:
        raise ValueError("Invalid move")

    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    # Determina e retorna o vencedor do jogo, se houver um
    for current_player in (X, O):
        # Verifica linhas, colunas e diagonais para uma vitória
        rows = board
        columns = [list(column) for column in zip(*board)]
        diagonals = [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]

        for line in rows + columns + diagonals:
            if line == [current_player] * 3:
                return current_player

    return None

def terminal(board):
    # Retorna True se o jogo terminou, False caso contrário
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    # Retorna 1 se X venceu, -1 se O venceu, ou 0 caso contrário
    win_player = winner(board)
    return 1 if win_player == X else -1 if win_player == O else 0

def minimax(board):
    # Determina e retorna a ação ótima para o jogador atual no tabuleiro
    if terminal(board):
        return None

    def max_value(board):
        # Calcula o valor máximo de uma jogada
        if terminal(board):
            return utility(board), None

        value = float('-inf')
        best_action = None
        for action in actions(board):
            val, _ = min_value(result(board, action))
            if val > value:
                value, best_action = val, action
        return value, best_action

    def min_value(board):
        # Calcula o valor mínimo de uma jogada
        if terminal(board):
            return utility(board), None

        value = float('inf')
        best_action = None
        for action in actions(board):
            val, _ = max_value(result(board, action))
            if val < value:
                value, best_action = val, action
        return value, best_action

    return max_value(board)[1] if player(board) == X else min_value(board)[1]