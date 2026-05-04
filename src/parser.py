from dataclasses import dataclass

@dataclass
class InputPuzzle:
    rows: int
    cols: int
    board: list[list[str]]
    costs: list[list[int]]

def parser_input_file(file_path: str) -> InputPuzzle:
    '''
    Format file:
    Baris Pertama: N M
    N baris berikutnya merepresentasikan papan
    N baris berikutnya merepresentasikan cost untuk melewati tile tersebut
    '''

    # Error handling saat buka file
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.rstrip("\n") for line in file if line.strip() != ""]
    except FileNotFoundError:
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    
    if len(lines) == 0:
        raise ValueError("File input kosong.")
    
    # Parser ukuran papan

    ukuran_papan = lines[0].split()

    if len(ukuran_papan) != 2:
        raise ValueError("Baris pertama harus berisi dua angka: N M.")
    
    try:
        rows = int(ukuran_papan[0])
        cols = int(ukuran_papan[1])
    except ValueError:
        raise ValueError("N dan M pada baris pertama harus berupa angka.")
    
    if rows <= 0 or cols <= 0:
        raise ValueError("N dan M harus berukuran lebih besar dari 0")
    
    # jumlah baris input minimal 1 ukuran papan + N baris papan + N baris cost

    jumlah_baris_input = 1 + rows + rows

    if len(lines) < jumlah_baris_input:
        raise ValueError(
            f"Jumlah baris kurang. Diperlukan {jumlah_baris_input} baris, hanya terdapat {len(lines)} baris.")
    
    # parser papan

    board_lines = lines[1:1+rows]
    board = []

    for i, line in enumerate(board_lines):
        if len(line) != cols:
            raise ValueError(f"Panjang baris board ke-{i + 1} tidak sesuai. Seharusnya {cols} tetapi ditemukan {len(line)}")
        board.append(list(line))

    # parser cost matrix

    cost_lines = lines[1+rows : 1+rows+rows]
    costs = []

    for i, line in enumerate(cost_lines):
        parts = line.split()
        if len(parts) != cols:
            raise ValueError(f"Jumlah cost board ke-{i+1} tidak sesuai. Seharusnya {cols} tetapi ditemukan {len(parts)}")
        
        try:
            cost_row = [int(value) for value in parts]
        except ValueError:
            raise ValueError(f"Cost pada baris ke-{i + 1} harus berupa angka.")

        costs.append(cost_row)

    return InputPuzzle(rows, cols, board, costs)

def print_parsed_input(puzzle: InputPuzzle) -> None:
    # Fungsi bantuan untuk mengecek apakah parser sudah benar.

    print(f"Ukuran board: {puzzle.rows} x {puzzle.cols}")

    print("\nBoard:")
    for row in puzzle.board:
        print("".join(row))

    print("\nCost:")
    for row in puzzle.costs:
        print(" ".join(map(str, row)))
