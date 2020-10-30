# check for total liberty
# check for randomness in valid moves
# u may have to return board wihout died pieces
from copy import deepcopy

BLACK_PIECES = 0
WHITE_PIECES = 0


def read_board(n=5, path='input.txt'):
    with open(path, 'r') as board_data_file:
        board_data = board_data_file.read().split('\n')
        board_data = [list(map(int, list(x))) for x in board_data]
        return board_data[0][0], board_data[1:n + 1], board_data[n + 1: 2 * n + 1]


def write_move(result, path='output.txt'):
    with open(path, 'w') as move_file:
        move_file.write(result if result == 'PASS' else ','.join(map(str, result[:2])))


def on_board(i, j, n=5):
    return True if 0 <= i < n and 0 <= j < n else False


def find_on_board_neighbours(i, j):
    neighbour_relative_coordinates = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    neighbours = [(i + del_x, j + del_y) for del_x, del_y in neighbour_relative_coordinates]
    return [neigh for neigh in neighbours if on_board(neigh[0], neigh[1])]


def find_neighbour_allies(i, j, board, player):
    neighbours = find_on_board_neighbours(i, j)
    return [neigh for neigh in neighbours if board[neigh[0]][neigh[1]] == player]


def get_all_ally_positions(i, j, board, player):
    stack = [(i, j)]
    all_allies = set()
    visited = set()
    while stack:
        piece = stack.pop()
        all_allies.add(piece)
        visited.add(piece)
        neighbor_allies = find_neighbour_allies(piece[0], piece[1], board, player)
        for neigh in neighbor_allies:
            if neigh not in visited and neigh not in all_allies:
                stack.append(neigh)

    return list(all_allies)


def have_liberty(i, j, board, player):
    my_all_allies = get_all_ally_positions(i, j, board, player)
    for ally in my_all_allies:
        neighbors = find_on_board_neighbours(ally[0], ally[1])
        for piece in neighbors:
            if board[piece[0]][piece[1]] == 0:
                return True
    return False


def find_died_pieces(player, board):
    died_pieces = []
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == player:
                if not have_liberty(i, j, board, player):
                    died_pieces.append((i, j))

    return died_pieces


def remove_died_pieces(died_pieces, board):
    for piece in died_pieces:
        board[piece[0]][piece[1]] = 0
    return board


def get_liberty_positions(i, j, board, player):
    available_positions = set()
    for member in get_all_ally_positions(i, j, board, player):
        neighbors = find_on_board_neighbours(member[0], member[1])
        available_positions.update([neigh for neigh in neighbors if board[neigh[0]][neigh[1]] == 0])

    return list(available_positions)


def get_neigh_liberty_positions(i, j, board):
    available_positions = set()
    available_positions.update(
        [neigh for neigh in find_on_board_neighbours(i, j) if board[neigh[0]][neigh[1]] == 0]
    )
    return list(available_positions)


def try_move(i, j, board, player):
    board[i][j] = player
    died_pieces = find_died_pieces(3 - player, board)
    new_board = deepcopy(board)
    for piece in died_pieces:
        new_board[piece[0]][piece[1]] = 0

    return board, len(died_pieces), new_board


def valid_moves(player, previous_board, new_board):
    moves = []
    imp_moves = []
    all_liberty_moves = set()

    for i in range(0, 5):
        for j in range(0, 5):
            if new_board[i][j] == player:
                self_end = get_liberty_positions(i, j, new_board, player)
                if len(self_end) == 1:
                    all_liberty_moves = all_liberty_moves | set(self_end)
                    if i == 0 or i == 4 or j == 0 or j == 4:
                        safe_positions = get_neigh_liberty_positions(self_end[0][0], self_end[0][1], new_board)
                        if safe_positions:
                            all_liberty_moves = all_liberty_moves | set(safe_positions)

            elif new_board[i][j] == 3 - player:
                oppo_end = get_liberty_positions(i, j, new_board, 3 - player)
                all_liberty_moves = all_liberty_moves | set(oppo_end)

    if len(list(all_liberty_moves)):
        for x in list(all_liberty_moves):
            tri_board = deepcopy(new_board)
            board_after_move, died_pieces, _ = try_move(x[0], x[1], tri_board, player)
            if have_liberty(x[0], x[1], board_after_move,
                            player) and board_after_move != new_board and board_after_move != previous_board:
                imp_moves.append((x[0], x[1], died_pieces))
        if len(imp_moves) != 0:
            return sorted(imp_moves, key=lambda x: x[2], reverse=True)

    for i in range(0, 5):
        for j in range(0, 5):
            if new_board[i][j] == 0:
                trial_board = deepcopy(new_board)
                board_after_move, died_pieces, _ = try_move(i, j, trial_board, player)
                if have_liberty(i, j, board_after_move,
                                player) and board_after_move != new_board and board_after_move != previous_board:
                    moves.append((i, j, died_pieces))

    return sorted(moves, key=lambda x: x[2], reverse=True)


def evaluation_function(board, player, died_pieces_black, died_pieces_white):
    black_count = 0
    white_count = 0
    black_endangered_liberty = 0
    white_endangered_liberty = 0
    white_total_liberty = set()
    black_total_liberty = set()
    # self_groups,oppo_groups=get_group_count_with_k_liberties(board,player,2)
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == 1:
                lib = get_liberty_positions(i, j, board, 1)
                # black_total_liberty=black_total_liberty | set(lib)
                if len(lib) <= 1:  # try 2
                    black_endangered_liberty = black_endangered_liberty + 1
                black_count += 1
            elif board[i][j] == 2:
                lib = get_liberty_positions(i, j, board, 2)
                # white_total_liberty=white_total_liberty | set(lib)
                if len(lib) <= 1:
                    white_endangered_liberty = white_endangered_liberty + 1
                white_count += 1
    white_count = white_count + 2.5
    if player == 1:
        eval_value = black_count - white_count + white_endangered_liberty - black_endangered_liberty + died_pieces_white * 10 - died_pieces_black * 16  # try my total-uska total liberty
    else:
        eval_value = -black_count + white_count - white_endangered_liberty + black_endangered_liberty + died_pieces_black * 10 - died_pieces_white * 16

    # eval_value=eval_value+oppo_groups-self_groups
    # print("player",player,eval_value)
    return eval_value


def best_move(board, previous_board, player, depth):
    died_pieces_white = 0
    score, actions = maximizer_value(board, previous_board, player, depth, float("-inf"), float("inf"), board)
    # print("yaar",score,actions)
    if len(actions) > 0:
        return actions[0]
    else:
        return "PASS"


def maximizer_value(board, previous_board, player, depth, alpha, beta, new_board_without_died_pieces):
    global BLACK_PIECES
    global WHITE_PIECES
    if player == 2:
        died_pieces_white = len(find_died_pieces(player, new_board_without_died_pieces))
        WHITE_PIECES = WHITE_PIECES + died_pieces_white
    if player == 1:
        died_pieces_black = len(find_died_pieces(player, new_board_without_died_pieces))
        BLACK_PIECES = BLACK_PIECES + died_pieces_black

    if depth == 0:
        value = evaluation_function(board, player, BLACK_PIECES, WHITE_PIECES)
        if player == 1:
            BLACK_PIECES = BLACK_PIECES - len(find_died_pieces(1, new_board_without_died_pieces))
        if player == 2:
            WHITE_PIECES = WHITE_PIECES - len(find_died_pieces(2, new_board_without_died_pieces))
        return value, []

    max_score = float("-inf")
    max_score_actions = []
    my_moves = valid_moves(player, previous_board, board)
    # print(type(my_moves))
    # print(len(my_moves))
    if len(my_moves) == 25:
        return 100, [(2, 2)]
    for move in my_moves:
        # print("idhar",move[0],move[1])
        trial_board = deepcopy(board)
        next_board, died_pieces, new_board_without_died_pieces = try_move(move[0], move[1], trial_board, player)
        # print("move max",move,died_pieces)
        score, actions = minimizer_value(next_board, board, 3 - player, depth - 1, alpha, beta,
                                         new_board_without_died_pieces)

        if score > max_score:
            max_score = score
            max_score_actions = [move] + actions

        if max_score > beta:
            return max_score, max_score_actions

        if max_score > alpha:
            alpha = max_score

    return max_score, max_score_actions


def minimizer_value(board, previous_board, player, depth, alpha, beta, new_board_without_died_pieces):
    global BLACK_PIECES
    global WHITE_PIECES
    if player == 2:
        died_pieces_white = len(find_died_pieces(player, new_board_without_died_pieces))
        WHITE_PIECES = WHITE_PIECES + died_pieces_white
    if player == 1:
        died_pieces_black = len(find_died_pieces(player, new_board_without_died_pieces))
        BLACK_PIECES = BLACK_PIECES + died_pieces_black

    if depth == 0:
        value = evaluation_function(board, player, BLACK_PIECES, WHITE_PIECES)
        if player == 1:
            BLACK_PIECES = BLACK_PIECES - len(find_died_pieces(1, new_board_without_died_pieces))
        if player == 2:
            WHITE_PIECES = WHITE_PIECES - len(find_died_pieces(2, new_board_without_died_pieces))
        return value, []

    min_score = float("inf")
    min_score_actions = []
    my_moves = valid_moves(player, previous_board, board)

    for move in my_moves:
        trial_board = deepcopy(board)
        next_board, died_pieces, new_board_without_died_pieces = try_move(move[0], move[1], trial_board, player)
        # print("move min",move,died_pieces)
        score, actions = maximizer_value(next_board, board, 3 - player, depth - 1, alpha, beta,
                                         new_board_without_died_pieces)
        # print("min",score,actions)

        if score < min_score:
            min_score = score
            min_score_actions = [move] + actions

        if min_score < alpha:
            return min_score, min_score_actions

        if min_score < beta:
            alpha = min_score

    return min_score, min_score_actions


def driver_function(player, previous_board, new_board):
    depth = 4
    # print(valid_moves(player, previous_board, new_board))
    # exit()
    good_move = best_move(new_board, previous_board, player, depth)
    # print(good_move)
    write_move(good_move)


player, previous_board, board = read_board()
driver_function(player, previous_board, board)