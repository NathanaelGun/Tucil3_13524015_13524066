import heapq
import time
from board import is_goal
from movement import get_valid_neighbors
from utils import reconstruct_path, make_result, SearchResult


def a_star_search(board_info, start_state, selected_heuristic) -> SearchResult:
    start_time = time.perf_counter()

    pq = []
    heap_id = 0

    best_cost = {start_state: 0}
    parent = {start_state: None}

    start_value = selected_heuristic(board_info, start_state)
    heapq.heappush(pq, (start_value, 0, heap_id, start_state))
    iterations = 0

    while pq:
        _, current_g, _, current_state = heapq.heappop(pq)
        iterations += 1

        if current_g != best_cost[current_state]:
            continue

        if is_goal(board_info, current_state):
            moves, states = reconstruct_path(parent, current_state)
            time_ms = (time.perf_counter() - start_time) * 1000
            return make_result(True, moves, states, best_cost[current_state], iterations, time_ms)

        for neighbor in get_valid_neighbors(board_info, current_state):
            next_state = neighbor.state
            new_cost = best_cost[current_state] + neighbor.move_cost

            if next_state not in best_cost or new_cost < best_cost[next_state]:
                best_cost[next_state] = new_cost
                parent[next_state] = (current_state, neighbor.direction)

                total_value = new_cost + selected_heuristic(board_info, next_state)
                heap_id += 1
                heapq.heappush(pq, (total_value, new_cost, heap_id, next_state))

    time_ms = (time.perf_counter() - start_time) * 1000
    return make_result(False, "", [], None, iterations, time_ms)
