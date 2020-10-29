class IOManager:
    @staticmethod
    def read_board(n, path='input.txt'):
        with open(path, 'r') as board_data_file:
            board_data = board_data_file.read().split('\n')
            board_data = [list(map(int, x.split(','))) for x in board_data]
            return board_data[0], board_data[1:n+1], board_data[n+1: 2*n + 1]

    @staticmethod
    def write_move(result, path='output.txt'):
        with open(path, 'w') as move_file:
            move_file.write(result if result == 'PASS' else ','.join(map(str, result)))


class GameHost:
    def __init__(self, board, player, n=5):
        self.board_size = n
        self.initial_board = board
        self.current_board = board
        self.previous_board = []
        self.my_player = player
        self.current_player = player
        self.neighbour_relative_coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def on_board(self, position):
        return True if 0 <= position[0] < self.board_size and 0 <= position[1] < self.board_size else False

    def find_on_board_neighbours(self, position):
        neighbours = [(position[0] + del_x, position[1] + del_y) for del_x, del_y in self.neighbour_relative_coordinates]
        return [neigh for neigh in neighbours if self.on_board(neigh)]

    def find_neighbour_allies(self, position):
        neighbours = self.find_on_board_neighbours(position)
        return [neigh for neigh in neighbours if self.current_board[neigh[0]][neigh[1]] == self.current_player]

    def get_all_ally_positions(self, position):
        allies = set()
        if self.on_board(position):
            queue = [position]
            visited = set()
            allies.add(position)
            while queue:
                ally_neighbours = self.get_all_ally_positions(queue.pop())
                for neigh in ally_neighbours:
                    if neigh not in visited:
                        visited.add(neigh)
                        allies.add(neigh)
                        queue.append(neigh)

        return list(allies)




