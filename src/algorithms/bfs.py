from collections import deque
import time
from board import is_goal
from movement import get_valid_neighbors
from utils import reconstruct_path, make_result, SearchResult

def breadth_first_search(board_info, start_state) -> SearchResult:
    start_time = time.perf_counter()

    queue = deque([start_state])
    visited = {start_state}
    parent = {start_state: None}
    path_cost = {start_state: 0}
    iterations = 0

    while queue:
        current_state = queue.popleft()
        iterations += 1

        if is_goal(board_info, current_state):
            moves, states = reconstruct_path(parent, current_state)
            time_ms = (time.perf_counter() - start_time) * 1000
            return make_result(True,
                               moves,
                               states,
                               path_cost[current_state],
                               iterations,
                               time_ms,)
        
        for neighbor in get_valid_neighbors(board_info, current_state):
            next_state = neighbor.state
            if next_state in visited:
                continue

            visited.add(next_state)
            parent[next_state] = (current_state, neighbor.direction)
            path_cost[next_state] = path_cost[current_state] + neighbor.move_cost
            queue.append(next_state)

    time_ms = (time.perf_counter() - start_time) * 1000
    return make_result(False, "", [], None, iterations, time_ms)

