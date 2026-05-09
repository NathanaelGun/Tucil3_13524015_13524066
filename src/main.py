from parser import parser_input_file
from validator import validate_puzzle
from board import create_board_info, create_state_awal
from algorithms.ucs import uniform_cost_search
from algorithms.gbfs import greedy_best_first_search
from algorithms.astar import a_star_search
from algorithms.bfs import breadth_first_search
from heuristic import choose_heuristic
from utils import print_result, playback, save_solution, get_input_path


def run_solver(board_info, start_state, algorithm: str):
    algorithm = algorithm.strip().upper()

    if algorithm == "UCS":
        return uniform_cost_search(board_info, start_state)

    if algorithm == "GBFS":
        print("Pilihan heuristic:")
        print("H1 = Manhattan")
        print("H2 = Pythagoras")
        print("H3 = Manhattan + checkpoint tersisa")
        print("H4 = Manhattan rantai checkpoint")
        print("H5 = Jarak minimum slide ke target berikutnya")
        heuristic_choice = input(">> Heuristic apa yang anda pilih? (H1/H2/H3/H4/H5): ").strip().upper()
        selected_heuristic = choose_heuristic(heuristic_choice)
        return greedy_best_first_search(board_info, start_state, selected_heuristic)

    if algorithm in {"A*", "ASTAR", "A-STAR"}:
        print("Pilihan heuristic:")
        print("H1 = Manhattan")
        print("H2 = Pythagoras")
        print("H3 = Manhattan + checkpoint tersisa")
        print("H4 = Manhattan rantai checkpoint")
        print("H5 = Jarak minimum slide ke target berikutnya")
        heuristic_choice = input(">> Heuristic apa yang anda pilih? (H1/H2/H3/H4/H5): ").strip().upper()
        selected_heuristic = choose_heuristic(heuristic_choice)
        return a_star_search(board_info, start_state, selected_heuristic)
    
    if algorithm == "BFS":
        return breadth_first_search(board_info, start_state)

    print("Karena input Algoritma yang kamu masukkan tidak tersedia, akan beralih ke Algoritma default 'UCS'.")
    return uniform_cost_search(board_info, start_state)


def main():
    file_path = get_input_path()

    try:
        puzzle = parser_input_file(file_path)
        validate_puzzle(puzzle)
        board_info = create_board_info(puzzle)
        start_state = create_state_awal(board_info)

        algorithm = input(">> Algoritma apa yang anda pilih? (UCS/GBFS/A*/BFS): ").strip().upper()

        result = run_solver(board_info, start_state, algorithm)

        print()
        print_result(board_info, result)

        if result.found:
            answer = input("\n>> Apakah Anda ingin melakukan playback? (Ya/Tidak): ").strip().lower()
            if answer in {"ya", "y", "iya"}:
                playback(board_info, result.states, result.moves)

        save_answer = input("\n>> Apakah Anda ingin menyimpan solusi? (Ya/Tidak): ").strip().lower()
        if save_answer in {"ya", "y", "iya"}:
            output_path = input(">> Masukkan path output: ").strip()
            save_solution(board_info, result, output_path)
            print(f">> Solusi disimpan pada {output_path}")
        else:
            print("Solusi tidak disimpan, program selesai.")

    except Exception as error:
        print(f"Input tidak valid: {error}")


if __name__ == "__main__":
    main()




# from parser import parser_input_file, print_parsed_input
# from validator import validate_puzzle
# from board import create_board_info, create_state_awal, print_board, is_goal
# from movement import DIRECTIONS, get_valid_neighbors, slide
# import sys


# def print_slide_result(result) -> None:
#     status = "valid" if result.valid else "tidak valid"
#     print(f"\nGerakan {result.direction}: {status}")
#     print(f"Cost gerakan: {result.move_cost}")

#     if result.passed_tiles:
#         print(f"Tile dilewati: {result.passed_tiles}")
#     else:
#         print("Tile dilewati: []")

#     if result.reason:
#         print(f"Alasan: {result.reason}")

#     if result.state is not None:
#         print(
#             "State akhir: "
#             f"row={result.state.row}, "
#             f"col={result.state.col}, "
#             f"next_checkpoint={result.state.next_checkpoint}"
#         )


# def print_valid_neighbors(board_info, state) -> None:
#     neighbors = get_valid_neighbors(board_info, state)
#     print("\nGerakan valid dari state ini:")

#     if not neighbors:
#         print("- Tidak ada gerakan valid.")
#         return

#     for neighbor in neighbors:
#         if neighbor.state is None:
#             continue

#         print(
#             f"- {neighbor.direction}: "
#             f"ke ({neighbor.state.row}, {neighbor.state.col}), "
#             f"cost={neighbor.move_cost}, "
#             f"next_checkpoint={neighbor.state.next_checkpoint}"
#         )


# def main():
#     if len(sys.argv) > 1:
#         file_path = sys.argv[1]
#     else:
#         file_path = input("Masukkan file input: ")

#     try:
#         puzzle = parser_input_file(file_path)
#         validate_puzzle(puzzle)
#         board_info = create_board_info(puzzle)
#         state = create_state_awal(board_info)

#         print("Input valid.\n")
#         print_parsed_input(puzzle)

#         print("\nBoard awal:")
#         print_board(board_info, state)

#         print(
#             "\nState awal: "
#             f"row={state.row}, col={state.col}, "
#             f"next_checkpoint={state.next_checkpoint}"
#         )

#         print_valid_neighbors(board_info, state)

#         while True:
#             command = input("\nMasukkan gerakan U/D/L/R, N untuk neighbors, Q untuk keluar: ")
#             command = command.strip().upper()

#             if command == "Q":
#                 break

#             if command == "N":
#                 print_valid_neighbors(board_info, state)
#                 continue

#             if command not in DIRECTIONS:
#                 print("Perintah tidak valid.")
#                 continue

#             result = slide(board_info, state, command)
#             print_slide_result(result)

#             if result.valid and result.state is not None:
#                 state = result.state
#                 print("\nBoard sekarang:")
#                 print_board(board_info, state)

#                 if is_goal(board_info, state):
#                     print("\nGoal tercapai.")
#                     break
#     except Exception as error:
#         print(f"Input tidak valid: {error}")

# if __name__ == "__main__":
#     main()
