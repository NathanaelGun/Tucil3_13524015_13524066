import math
from collections import deque
from board import BoardInfo, State
from movement import get_valid_neighbors


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


def h4_checkpoint_chain_manhattan(board_info: BoardInfo, state: State) -> float:
    min_cost = get_min_traversable_cost(board_info)
    points = [(state.row, state.col)]

    checkpoint_number = state.next_checkpoint
    while checkpoint_number in board_info.checkpoints:
        points.append(board_info.checkpoints[checkpoint_number])
        checkpoint_number += 1

    points.append(board_info.goal)

    total_distance = 0
    for i in range(len(points) - 1):
        row_a, col_a = points[i]
        row_b, col_b = points[i + 1]
        total_distance += abs(row_a - row_b) + abs(col_a - col_b)

    return total_distance * min_cost


def h5_sliding_move_distance(board_info: BoardInfo, state: State) -> float:
    target = get_current_target(board_info, state)
    min_cost = get_min_traversable_cost(board_info)

    queue = deque([(state, 0)])
    visited = {state}

    while queue:
        current_state, slide_count = queue.popleft()

        if (current_state.row, current_state.col) == target:
            return slide_count * min_cost

        for neighbor in get_valid_neighbors(board_info, current_state):
            next_state = neighbor.state
            if next_state in visited:
                continue

            visited.add(next_state)
            queue.append((next_state, slide_count + 1))

    return 0


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
    if choice == "H4":
        return h4_checkpoint_chain_manhattan
    if choice == "H5":
        return h5_sliding_move_distance
    if choice in {"H0", "ZERO"}:
        return h0_zero

    print("Karena input Heuristic yang kamu masukkan tidak tersedia, akan beralih ke Heuristic default 'H1'.")
    return h1_manhattan
