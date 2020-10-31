from copy import deepcopy


class IOManager:
    @staticmethod
    def read_board(n=5, path='input.txt'):
        with open(path, 'r') as board_data_file:
            board_data = board_data_file.read().split('\n')
            board_data = [list(map(int, list(x))) for x in board_data]
            return board_data[0][0], board_data[1:n+1], board_data[n+1: 2*n + 1]

    @staticmethod
    def write_move(result, path='output.txt'):
        with open(path, 'w') as move_file:
            move_file.write(result if result == 'PASS' else ','.join(map(str, result[:2])))


class GameHost:
    def __init__(self, previous_board, current_board, player, n=5):
        self.board_size = n
        self.initial_board = current_board
        self.current_board = current_board
        self.previous_board = previous_board
        self.my_player = player
        self.current_player = player
        self.neighbour_relative_coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def on_board(self, position):
        return True if 0 <= position[0] < self.board_size and 0 <= position[1] < self.board_size else False

    def find_on_board_neighbours(self, position):
        neighbours = [(position[0] + del_x, position[1] + del_y) for del_x, del_y in self.neighbour_relative_coordinates]
        return [neigh for neigh in neighbours if self.on_board(neigh)]

    def find_neighbour_allies(self, position, board, player):
        neighbours = self.find_on_board_neighbours(position)
        return [neigh for neigh in neighbours if board[neigh[0]][neigh[1]] == player]

    def get_all_ally_positions(self, position, board, player):
        stack = [position]
        all_allies = set()
        visited = set()
        while stack:
            piece = stack.pop()
            all_allies.add(piece)
            neighbor_allies = self.find_neighbour_allies(position=piece, board=board, player=player)
            for neigh in neighbor_allies:
                if neigh not in visited and neigh not in all_allies:
                    stack.append(neigh)
                    visited.add(piece)

        return list(all_allies)

    def have_liberty(self, position, board, player):
        all_allies = self.get_all_ally_positions(position=position, board=board, player=player)
        for member in all_allies:
            neighbors = self.find_on_board_neighbours(member)
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    return True

        return False

    def find_died_pieces(self, board, player):
        died_pieces = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == player and not self.have_liberty((i, j), board, player):
                    died_pieces.append((i, j))

        return died_pieces

    def get_liberty_positions(self, position, board, player):
        available_positions = set()
        for member in self.get_all_ally_positions(position=position, board=board, player=player):
            neighbors = self.find_on_board_neighbours(member)
            available_positions.update([neigh for neigh in neighbors if board[neigh[0]][neigh[1]] == 0])

        return list(available_positions)

    def check_move_validity_score(self, position, board, player):
        board[position[0]][position[1]] = player
        died_pieces = self.find_died_pieces(board=board, player=3 - player)
        new_board = board
        for piece in died_pieces:
            new_board[piece[0]][piece[1]] = 0

        return new_board, len(died_pieces), board

    def get_all_liberty_moves(self, new_board, player):
        all_liberty_moves = set()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if new_board[i][j] == player:
                    last = self.get_liberty_positions((i, j), new_board, player)
                    if len(last) == 1:
                        all_liberty_moves.update(last)
                        if i == 0 or i == 4 or j == 0 or j == 4:
                            available_places = set()
                            available_places.update(
                                [neigh for neigh in self.find_on_board_neighbours((last[0][0], last[0][1])) if new_board[neigh[0]][neigh[1]] == 0]
                            )
                            if available_places:
                                all_liberty_moves.update(available_places)

                elif new_board[i][j] == 3 - player:
                    end_2 = self.get_liberty_positions((i, j), new_board, 3 - player)
                    all_liberty_moves.update(end_2)

        return list(all_liberty_moves)

    def get_poss_move(self, previous_board, new_board, player):
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if new_board[i][j] == 0:
                    trial_board = deepcopy(new_board)
                    board_after_move, died_pieces, _ = self.check_move_validity_score((i, j), trial_board, player)
                    if self.have_liberty((i, j), board_after_move, player) and board_after_move != new_board and board_after_move != previous_board:
                        moves.append((i, j, died_pieces))

        return moves

    def get_legit_moves(self, previous_board, new_board, player, all_liberty_moves):
        legit_moves = []
        for x in all_liberty_moves:
            trial = deepcopy(new_board)
            tried_move_b, died_pieces, _ = self.check_move_validity_score((x[0], x[1]), trial, player)
            if self.have_liberty((x[0], x[1]), tried_move_b, player) and tried_move_b != new_board and tried_move_b != previous_board:
                legit_moves.append((x[0], x[1], died_pieces))

        if len(legit_moves) == 0:
            legit_moves = self.get_poss_move(previous_board, new_board, player)

        return legit_moves

    def get_moves(self, player, previous_board, new_board):
        return sorted(
            self.get_legit_moves(
                previous_board,
                new_board,
                player,
                self.get_all_liberty_moves(
                    new_board,
                    player
                )
            ),
            key=lambda x: x[2],
            reverse=True
        )
