import os
import sys
from dataclasses import dataclass
from board import render_board


@dataclass
class SearchResult:
    found: bool
    moves: str
    states: list
    cost: int | None
    iterations: int
    time_ms: float


def reconstruct_path(parent: dict, goal_state):
    moves = []
    states = [goal_state]
    current = goal_state

    while parent[current] is not None:
        previous_state, move = parent[current]
        moves.append(move)
        states.append(previous_state)
        current = previous_state

    moves.reverse()
    states.reverse()
    return "".join(moves), states


def make_result(found: bool, moves: str, states: list, cost, iterations: int, time_ms: float):
    return SearchResult(found, moves, states, cost, iterations, time_ms)


def print_result(board_info, result):
    if not result.found:
        print("Solusi tidak ditemukan.")
    
    else:
        print(f"Solusi Yang Ditemukan : {result.moves}")
        print(f"Cost dari Solusi : {result.cost}")

        print("\nInitial")
        print(render_board(board_info, result.states[0]))

        for i, move in enumerate(result.moves, start=1):
            print(f"\nStep {i} : {move}")
            print(render_board(board_info, result.states[i]))

    print(f"\n>> Waktu eksekusi: {result.time_ms:.3f} ms")
    print(f">> Banyak iterasi yang dilakukan: {result.iterations} iterasi")


def playback(board_info, states, moves):
    if not states:
        print("Tidak ada state untuk playback.")
        return

    index = 0

    while True:
        if index == 0:
            label = "Initial"
        else:
            label = f"Step {index} : {moves[index - 1]}"
        print(f"\n{label}")
        print(render_board(board_info, states[index]))
        print(f"Posisi playback: {index}/{len(states) - 1}")

        command = input("Playback - N next, P previous, angka step, Q keluar: ").strip().upper()

        if command == "Q":  
            break
        if command == "N":
            index = min(index + 1, len(states) - 1)
        elif command == "P":
            index = max(index - 1, 0)
        elif command.isdigit():
            target = int(command)
            if 0 <= target < len(states):
                index = target
            else:
                print("Nomor step di luar range.")
        else:
            print("Perintah tidak valid.")


def save_solution(board_info, result, output_filename: str):
    output_dir = "test/output"
    os.makedirs(output_dir, exist_ok=True)

    if not output_filename.endswith(".txt"):
        output_filename += ".txt"
    
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as file:
        if not result.found:
            file.write("Solusi tidak ditemukan.\n")
            file.write(f"Waktu eksekusi: {result.time_ms:.3f} ms\n")
            file.write(f"Banyak iterasi: {result.iterations} iterasi\n")
            return

        file.write(f"Solusi Yang Ditemukan : {result.moves}\n")
        file.write(f"Cost dari Solusi : {result.cost}\n")
        file.write(f"Waktu eksekusi: {result.time_ms:.3f} ms\n")
        file.write(f"Banyak iterasi: {result.iterations} iterasi\n\n")

        file.write("Initial\n")
        file.write(render_board(board_info, result.states[0]) + "\n")

        for i, move in enumerate(result.moves, start=1):
            file.write(f"\nStep {i} : {move}\n")
            file.write(render_board(board_info, result.states[i]) + "\n")

def get_input_path():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input(">> Masukan nama file input: ").strip()

    if not filename.endswith(".txt"):
        filename += ".txt"

    if os.path.dirname(filename):
        return filename

    return os.path.join("test","input", filename)
