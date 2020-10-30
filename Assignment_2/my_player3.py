from utils import *


class Agent:
    def __init__(self, my_player, previous_board, current_board):
        self.previous_board = previous_board
        self.current_board = current_board
        self.my_player = my_player
        self.depth = 4
        self.game_host = GameHost(previous_board=previous_board, current_board=current_board, player=my_player)
        self.BLACK_PIECES = 0
        self.WHITE_PIECES = 0

    def heuristic_score(self, board, player, died_pieces_black, died_pieces_white):
        black_count = 0
        white_count = 0
        black_endangered_liberty = 0
        white_endangered_liberty = 0
        for i in range(0, 5):
            for j in range(0, 5):
                if board[i][j] == 1:
                    lib = self.game_host.get_liberty_positions((i, j), board, 1)
                    if len(lib) <= 1:
                        black_endangered_liberty = black_endangered_liberty + 1
                    black_count += 1
                elif board[i][j] == 2:
                    lib = self.game_host.get_liberty_positions((i, j), board, 2)
                    if len(lib) <= 1:
                        white_endangered_liberty = white_endangered_liberty + 1
                    white_count += 1
        white_count = white_count + 2.5
        if player == 1:
            eval_value = black_count-white_count+white_endangered_liberty-black_endangered_liberty+died_pieces_white*10-died_pieces_black*16
        else:
            eval_value = -black_count + white_count-white_endangered_liberty+black_endangered_liberty+died_pieces_black*10-died_pieces_white*16

        return eval_value

    def max_move(self, board, previous_board, player, depth, alpha, beta, new_board_without_died_pieces):
        if player == 2:
            died_pieces_white = len(self.game_host.find_died_pieces(new_board_without_died_pieces, player))
            self.WHITE_PIECES = self.WHITE_PIECES + died_pieces_white
        if player == 1:
            died_pieces_black = len(self.game_host.find_died_pieces(new_board_without_died_pieces, player))
            self.BLACK_PIECES = self.BLACK_PIECES + died_pieces_black

        if depth == 0:
            value = self.heuristic_score(board, player, self.BLACK_PIECES, self.WHITE_PIECES)
            if player == 1:
                self.BLACK_PIECES = self.BLACK_PIECES - len(self.game_host.find_died_pieces(new_board_without_died_pieces, 1))
            if player == 2:
                self.WHITE_PIECES = self.WHITE_PIECES - len(self.game_host.find_died_pieces(new_board_without_died_pieces, 2))
            return value, []

        max_score = float("-inf")
        max_score_actions = []
        my_moves = self.game_host.valid_moves(player, previous_board, board)
        if len(my_moves) == 25:
            return 100, [(2, 2)]

        for move in my_moves:
            trial_board = deepcopy(board)
            next_board, died_pieces, new_board_without_died_pieces = self.game_host.try_move((move[0], move[1]), trial_board, player)
            score, actions = self.min_move(
                next_board, board, 3 - player, depth - 1, alpha, beta, new_board_without_died_pieces
            )

            if score > max_score:
                max_score = score
                max_score_actions = [move] + actions

            if max_score > beta:
                return max_score, max_score_actions

            if max_score > alpha:
                alpha = max_score

        return max_score, max_score_actions

    def min_move(self, board, previous_board, player, depth, alpha, beta, new_board_without_died_pieces):
        if player == 2:
            died_pieces_white = len(self.game_host.find_died_pieces(new_board_without_died_pieces, player))
            self.WHITE_PIECES = self.WHITE_PIECES + died_pieces_white
        if player == 1:
            died_pieces_black = len(self.game_host.find_died_pieces(new_board_without_died_pieces, player))
            self.BLACK_PIECES = self.BLACK_PIECES + died_pieces_black

        if depth == 0:
            value = self.heuristic_score(board, player, self.BLACK_PIECES, self.WHITE_PIECES)
            if player == 1:
                self.BLACK_PIECES = self.BLACK_PIECES - len(self.game_host.find_died_pieces(new_board_without_died_pieces, 1))
            if player == 2:
                self.WHITE_PIECES = self.WHITE_PIECES - len(self.game_host.find_died_pieces(new_board_without_died_pieces, 2))
            return value, []

        min_score = float("inf")
        min_score_actions = []
        my_moves = self.game_host.valid_moves(player, previous_board, board)

        for move in my_moves:
            trial_board = deepcopy(board)
            next_board, died_pieces, new_board_without_died_pieces = self.game_host.try_move((move[0], move[1]), trial_board, player)
            score, actions = self.max_move(
                next_board, board, 3 - player, depth - 1, alpha, beta, new_board_without_died_pieces
            )

            if score < min_score:
                min_score = score
                min_score_actions = [move] + actions

            if min_score < alpha:
                return min_score, min_score_actions

            if min_score < beta:
                alpha = min_score

        return min_score, min_score_actions

    def play(self):
        score, actions = self.max_move(
            self.current_board,
            self.previous_board,
            self.my_player,
            self.depth,
            float("-inf"),
            float("inf"),
            self.current_board
        )
        IOManager.write_move(actions[0] if len(actions) > 0 else 'PASS')


if __name__ == '__main__':
    player, previous_board, board = IOManager.read_board()
    Agent(player, previous_board, board).play()
