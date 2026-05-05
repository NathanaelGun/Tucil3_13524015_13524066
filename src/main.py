from parser import parser_input_file, print_parsed_input
from validator import validate_puzzle
from board import create_board_info, create_state_awal, print_board, is_goal
from movement import DIRECTIONS, get_valid_neighbors, slide
import sys


def print_slide_result(result) -> None:
    status = "valid" if result.valid else "tidak valid"
    print(f"\nGerakan {result.direction}: {status}")
    print(f"Cost gerakan: {result.move_cost}")

    if result.passed_tiles:
        print(f"Tile dilewati: {result.passed_tiles}")
    else:
        print("Tile dilewati: []")

    if result.reason:
        print(f"Alasan: {result.reason}")

    if result.state is not None:
        print(
            "State akhir: "
            f"row={result.state.row}, "
            f"col={result.state.col}, "
            f"next_checkpoint={result.state.next_checkpoint}"
        )


def print_valid_neighbors(board_info, state) -> None:
    neighbors = get_valid_neighbors(board_info, state)
    print("\nGerakan valid dari state ini:")

    if not neighbors:
        print("- Tidak ada gerakan valid.")
        return

    for neighbor in neighbors:
        if neighbor.state is None:
            continue

        print(
            f"- {neighbor.direction}: "
            f"ke ({neighbor.state.row}, {neighbor.state.col}), "
            f"cost={neighbor.move_cost}, "
            f"next_checkpoint={neighbor.state.next_checkpoint}"
        )


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Masukkan file input: ")

    try:
        puzzle = parser_input_file(file_path)
        validate_puzzle(puzzle)
        board_info = create_board_info(puzzle)
        state = create_state_awal(board_info)

        print("Input valid.\n")
        print_parsed_input(puzzle)

        print("\nBoard awal:")
        print_board(board_info, state)

        print(
            "\nState awal: "
            f"row={state.row}, col={state.col}, "
            f"next_checkpoint={state.next_checkpoint}"
        )

        print_valid_neighbors(board_info, state)

        while True:
            command = input("\nMasukkan gerakan U/D/L/R, N untuk neighbors, Q untuk keluar: ")
            command = command.strip().upper()

            if command == "Q":
                break

            if command == "N":
                print_valid_neighbors(board_info, state)
                continue

            if command not in DIRECTIONS:
                print("Perintah tidak valid.")
                continue

            result = slide(board_info, state, command)
            print_slide_result(result)

            if result.valid and result.state is not None:
                state = result.state
                print("\nBoard sekarang:")
                print_board(board_info, state)

                if is_goal(board_info, state):
                    print("\nGoal tercapai.")
                    break
    except Exception as error:
        print(f"Input tidak valid: {error}")

if __name__ == "__main__":
    main()
