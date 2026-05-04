from parser import parser_input_file, print_parsed_input
from validator import validate_puzzle

def main():
    file_path = input("Masukkan file input: ")

    try:
        puzzle = parser_input_file(file_path)
        validate_puzzle(puzzle)

        print("Input valid.\n")
        print_parsed_input(puzzle)
    except Exception as error:
        print(f"Input tidak valid: {error}")

if __name__ == "__main__":
    main()