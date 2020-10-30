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
            visited.add(piece)
            neighbor_allies = self.find_neighbour_allies(piece, board, player)
            for neigh in neighbor_allies:
                if neigh not in visited and neigh not in all_allies:
                    stack.append(neigh)

        return list(all_allies)

        # allies = set()
        # if self.on_board(position):
        #     queue = [position]
        #     visited = set()
        #     allies.add(position)
        #     while queue:
        #         ally_neighbours = self.find_neighbour_allies(queue.pop(), board, player)
        #         for neigh in ally_neighbours:
        #             if neigh not in visited:
        #                 visited.add(neigh)
        #                 allies.add(neigh)
        #                 queue.append(neigh)
        #
        # return list(allies)

    def have_liberty(self, position, board, player):
        all_allies = self.get_all_ally_positions(position, board, player)
        for member in all_allies:
            neighbors = self.find_on_board_neighbours(member)
            for piece in neighbors:
                if board[piece[0]][piece[1]] == 0:
                    return True

        return False

    def find_died_pieces(self, board, player):
        died_pieces = []
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if board[i][j] == player:

                    if not self.have_liberty((i, j), board, player):
                        died_pieces.append((i, j))

        return died_pieces

    def get_liberty_positions(self, position, board, player):
        available_positions = set()
        for member in self.get_all_ally_positions(position, board, player):
            neighbors = self.find_on_board_neighbours(member)
            available_positions.update([neigh for neigh in neighbors if board[neigh[0]][neigh[1]] == 0])

        return list(available_positions)

    def get_neigh_liberty_positions(self, position, board):
        available_positions = set()
        available_positions.update(
            [neigh for neigh in self.find_on_board_neighbours(position) if board[neigh[0]][neigh[1]] == 0]
        )
        return list(available_positions)

    def try_move(self, position, board, player):
        board[position[0]][position[1]] = player
        new_board = deepcopy(board)
        died_pieces = self.find_died_pieces(board, 3 - player)
        for piece in died_pieces:
            new_board[piece[0]][piece[1]] = 0

        return new_board, len(died_pieces), board

    # todo: remove code for debugging
    def valid_moves(self, player, previous_board, new_board):
        moves = []
        imp_moves = []
        all_liberty_moves = set()

        for i in range(0, 5):
            for j in range(0, 5):
                if new_board[i][j] == player:
                    self_end = self.get_liberty_positions((i, j), new_board, player)
                    if len(self_end) == 1:
                        all_liberty_moves = all_liberty_moves | set(self_end)
                        if i == 0 or i == 4 or j == 0 or j == 4:
                            safe_positions = self.get_neigh_liberty_positions(
                                (self_end[0][0], self_end[0][1]), new_board
                            )
                            if safe_positions:
                                all_liberty_moves = all_liberty_moves | set(safe_positions)

                elif new_board[i][j] == 3 - player:
                    oppo_end = self.get_liberty_positions((i, j), new_board, 3 - player)
                    all_liberty_moves = all_liberty_moves | set(oppo_end)

        if len(list(all_liberty_moves)):
            for x in list(all_liberty_moves):
                tri_board = deepcopy(new_board)
                board_after_move, died_pieces, _ = self.try_move((x[0], x[1]), tri_board, player)
                if self.have_liberty((x[0], x[1]), board_after_move, player) and board_after_move != new_board and board_after_move != previous_board:
                    imp_moves.append((x[0], x[1], died_pieces))

            if len(imp_moves) != 0:
                return sorted(imp_moves, key=lambda x: x[2], reverse=True)

        for i in range(0, 5):
            for j in range(0, 5):

                if new_board[i][j] == 0:

                    trial_board = deepcopy(new_board)
                    board_after_move, died_pieces, _ = self.try_move((i, j), trial_board, player)
                    if self.have_liberty((i, j), board_after_move, player) and board_after_move != new_board and board_after_move != previous_board:
                        moves.append((i, j, died_pieces))

        return sorted(moves, key=lambda x: x[2], reverse=True)
