import heapq
import time
from board import is_goal
from movement import get_valid_neighbors
from utils import reconstruct_path, make_result, SearchResult


def greedy_best_first_search(board_info, start_state, selected_heuristic) -> SearchResult:
    start_time = time.perf_counter()

    pq = []
    heap_id = 0
    heapq.heappush(pq, (selected_heuristic(board_info, start_state), heap_id, start_state))

    parent = {start_state: None}
    path_cost = {start_state: 0}
    visited = set()
    iterations = 0

    while pq:
        _, _, current_state = heapq.heappop(pq)
        iterations += 1

        if current_state in visited:
            continue
        visited.add(current_state)

        if is_goal(board_info, current_state):
            moves, states = reconstruct_path(parent, current_state)
            time_ms = (time.perf_counter() - start_time) * 1000
            return make_result(True, moves, states, path_cost[current_state], iterations, time_ms)

        for neighbor in get_valid_neighbors(board_info, current_state):
            next_state = neighbor.state

            if next_state in visited or next_state in parent:
                continue

            parent[next_state] = (current_state, neighbor.direction)
            path_cost[next_state] = path_cost[current_state] + neighbor.move_cost

            heap_id += 1
            heapq.heappush(pq, (selected_heuristic(board_info, next_state), heap_id, next_state))

    time_ms = (time.perf_counter() - start_time) * 1000
    return make_result(False, "", [], None, iterations, time_ms)
