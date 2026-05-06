import math
from board import BoardInfo, State


def get_min_traversable_cost(board_info: BoardInfo) -> int:
    min_cost = float("inf")

    for r in range(board_info.rows):
        for c in range(board_info.cols):
            tile = board_info.board[r][c]
            if tile not in {"X", "L"}:
                min_cost = min(min_cost, board_info.costs[r][c])

    if min_cost == float("inf"):
        return 0
    return min_cost


def get_current_target(board_info: BoardInfo, state: State) -> tuple[int, int]:
    if state.next_checkpoint in board_info.checkpoints:
        return board_info.checkpoints[state.next_checkpoint]
    return board_info.goal


def h1_manhattan(board_info: BoardInfo, state: State) -> float:
    target_row, target_col = get_current_target(board_info, state)
    min_cost = get_min_traversable_cost(board_info)
    distance = abs(state.row - target_row) + abs(state.col - target_col)
    return distance * min_cost


def h2_pythagoras(board_info: BoardInfo, state: State) -> float:
    target_row, target_col = get_current_target(board_info, state)
    min_cost = get_min_traversable_cost(board_info)
    distance = math.sqrt((state.row - target_row) ** 2 + (state.col - target_col) ** 2)
    return distance * min_cost


#idenya ni manhattan + banyak checkpoint yang ada (jadi targetnya kalo ada checkpoint lebi
#fokus ngerjain itu dulu
def h3_manhattan_checkpoint(board_info: BoardInfo, state: State) -> float:
    target_row, target_col = get_current_target(board_info, state)
    min_cost = get_min_traversable_cost(board_info)
    distance = abs(state.row - target_row) + abs(state.col - target_col)
    remaining = max(0, len(board_info.checkpoints) - state.next_checkpoint)
    return (distance + remaining) * min_cost


def h0_zero(board_info: BoardInfo, state: State) -> float:
    return 0


def choose_heuristic(choice: str):
    choice = choice.upper().strip()

    if choice == "H1":
        return h1_manhattan
    if choice == "H2":
        return h2_pythagoras
    if choice == "H3":
        return h3_manhattan_checkpoint
    if choice in {"H0", "ZERO"}:
        return h0_zero

    print("Karena input Heuristic yang kamu masukkan tidak tersedia, akan beralih ke Heuristic default 'H1'.")
    return h1_manhattan
