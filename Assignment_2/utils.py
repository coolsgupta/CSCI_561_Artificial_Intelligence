class Utils:
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
    def __init__(self, n=5):
        self.board_size = n
        self.current_board = []
        self.previous_board = []
        self.player_side = 0
        self.neighbour_relative_coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]

    def on_board(self, x, y):
        return True if 0 <= x < self.board_size and 0 <= y < self.board_size else False

    def find_on_board_neighbours(self, x, y):
        neighbours = [(x+del_x, y+del_y) for del_x, del_y in self.neighbour_relative_coordinates]
        return [neighbour for neighbour in neighbours if self.on_board(neighbour[0], neighbour[1])]




