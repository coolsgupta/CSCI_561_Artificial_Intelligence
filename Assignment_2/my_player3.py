from utils import *


class Agent:
    def __init__(self):
        self.get_host()
        self.board_size = 5
        self.tree_depth_leeway = 4
        self.komi = 2.5
        self.score_black = 0
        self.score_white = 0

    def get_host(self):
        my_player, previous_board, current_board = IOManager.read_board()
        self.previous_board = previous_board
        self.current_board = current_board
        self.my_player = my_player
        self.game_host = GameHost(
            previous_board=previous_board,
            current_board=current_board,
            player=my_player
        )

    def heuristic_score(self, board, player, died_pieces_black, died_pieces_white):
        score_black, score_white, danger_black, danger_white = 0, self.komi, 0, 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 1:
                    score_black += 1
                    available_liberty = self.game_host.get_liberty_positions((i, j), board, 1)
                    if len(available_liberty) <= 1:
                        danger_black += 1

                elif board[i][j] == 2:
                    score_white += 1
                    available_liberty = self.game_host.get_liberty_positions((i, j), board, 2)
                    if len(available_liberty) <= 1:
                        danger_white += 1

        if player == 1:
            heuristic_score = score_black-score_white+danger_white-danger_black+died_pieces_white*10-died_pieces_black*16
        else:
            heuristic_score = -score_black + score_white-danger_white+danger_black+died_pieces_black*10-died_pieces_white*16

        return heuristic_score

    def max_move(self, **kwargs):
        board = kwargs.get('board')
        previous_board = kwargs.get('previous_board')
        player = kwargs.get('player')
        tree_depth_leeway = kwargs.get('tree_depth_leeway')
        alpha = kwargs.get('alpha')
        beta = kwargs.get('beta')
        board_retain_pieces = kwargs.get('board_retain_pieces')

        if player == 2:
            self.score_white += len(self.game_host.find_died_pieces(board_retain_pieces, player))

        if player == 1:
            self.score_black += len(self.game_host.find_died_pieces(board_retain_pieces, player))

        if tree_depth_leeway < 1:
            value = self.heuristic_score(board, player, self.score_black, self.score_white)
            if player == 1:
                self.score_black -= len(self.game_host.find_died_pieces(board_retain_pieces, 1))
            if player == 2:
                self.score_white -= len(self.game_host.find_died_pieces(board_retain_pieces, 2))

            new_alpha_max_val, available_actions = value, []

        else:
            new_alpha_max_val = float("-inf")
            available_actions = []
            my_moves = self.game_host.get_moves(player, previous_board, board)
            if len(my_moves) == 25:
                return 100, [(2, 2)]

            for move in my_moves:
                trial_board = deepcopy(board)
                next_board, died_pieces, board_retain_pieces = self.game_host.check_move_validity_score((move[0], move[1]), trial_board, player)
                score, actions = self.min_move(
                    board=next_board,
                    previous_board=board,
                    player=3 - player,
                    tree_depth_leeway=tree_depth_leeway - 1,
                    alpha=alpha,
                    beta=beta,
                    board_retain_pieces=board_retain_pieces
                )

                if score > new_alpha_max_val:
                    new_alpha_max_val = score
                    available_actions = [move] + actions

                if new_alpha_max_val > beta:
                    break

                if new_alpha_max_val > alpha:
                    alpha = new_alpha_max_val

        return new_alpha_max_val, available_actions

    def min_move(self, **kwargs):
        board = kwargs.get('board')
        previous_board = kwargs.get('previous_board')
        player = kwargs.get('player')
        tree_depth_leeway = kwargs.get('tree_depth_leeway')
        alpha = kwargs.get('alpha')
        beta = kwargs.get('beta')
        board_retain_pieces = kwargs.get('board_retain_pieces')

        if player == 2:
            self.score_white += len(self.game_host.find_died_pieces(board_retain_pieces, player))

        if player == 1:
            self.score_black += len(self.game_host.find_died_pieces(board_retain_pieces, player))

        if tree_depth_leeway < 1:
            value = self.heuristic_score(board, player, self.score_black, self.score_white)
            if player == 1:
                self.score_black -= len(self.game_host.find_died_pieces(board_retain_pieces, 1))
            if player == 2:
                self.score_white -= len(self.game_host.find_died_pieces(board_retain_pieces, 2))

            new_beta_min_val, available_actions = value, []

        else:
            new_beta_min_val = float("inf")
            available_actions = []
            my_moves = self.game_host.get_moves(player, previous_board, board)

            for move in my_moves:
                trial_board = deepcopy(board)
                next_board, died_pieces, board_retain_pieces = self.game_host.check_move_validity_score((move[0], move[1]), trial_board, player)
                score, actions = self.max_move(
                    board=next_board,
                    previous_board=board,
                    player=3 - player,
                    tree_depth_leeway=tree_depth_leeway - 1,
                    alpha=alpha,
                    beta=beta,
                    board_retain_pieces=board_retain_pieces
                )
                if score < new_beta_min_val:
                    new_beta_min_val = score
                    available_actions = [move] + actions

                if new_beta_min_val < alpha:
                    break

                if new_beta_min_val < beta:
                    alpha = new_beta_min_val

        return new_beta_min_val, available_actions

    def play(self):
        score, actions = self.max_move(
            board=self.current_board,
            previous_board=self.previous_board,
            player=self.my_player,
            tree_depth_leeway=self.tree_depth_leeway,
            alpha=float("-inf"),
            beta=float("inf"),
            board_retain_pieces=self.current_board
        )
        IOManager.write_move(actions[0] if len(actions) > 0 else 'PASS')


if __name__ == '__main__':
    Agent().play()
