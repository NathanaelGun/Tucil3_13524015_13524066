VALID_TILES = {"X", "*", "L", "Z", "O"} | set("0123456789")

def validate_puzzle(puzzle) -> None:
    validate_board_size(puzzle)
    validate_board_characters(puzzle)
    validate_start_and_goal(puzzle)
    validate_checkpoints(puzzle)
    validate_costs(puzzle)

def validate_board_size(puzzle) -> None:
    if len(puzzle.board) != puzzle.rows:
        raise ValueError("Jumlah baris board tidak sesuai dengan N.")

    for i, row in enumerate(puzzle.board):
        if len(row) != puzzle.cols:
            raise ValueError(f"Panjang baris board ke-{i+1} tidak sesuai dengan M")
        
    if len(puzzle.costs) != puzzle.rows:
        raise ValueError("Jumlah baris cost tidak sesuai dengan N.")

    for i, row in enumerate(puzzle.costs):
        if len(row) != puzzle.cols:
            raise ValueError(f"Jumlah cost pada baris ke-{i + 1} tidak sesuai dengan M.")

def validate_board_characters(puzzle) -> None:
    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            tile = puzzle.board[r][c]
            if tile not in VALID_TILES:
                raise ValueError(f"Karakter tidak valid '{tile}' ditemukan di posisi ({r}, {c})")
            
def validate_start_and_goal(puzzle) -> None:
    start_count = 0
    goal_count = 0
    for row in puzzle.board:
        for tile in row :
            if tile == "Z":
                start_count += 1
            elif tile == "O":
                goal_count += 1

    if start_count != 1:
        raise ValueError(
            f"Jumlah Z harus tepat 1, tetapi ditemukan {start_count}."
        )

    if goal_count != 1:
        raise ValueError(
            f"Jumlah tujuan O harus tepat 1, tetapi ditemukan {goal_count}."
        )


def validate_checkpoints(puzzle) -> None:
    checkpoints = set()

    for row in puzzle.board:
        for tile in row:
            if tile.isdigit():
                checkpoints.add(int(tile))

    if not checkpoints:
        return

    max_checkpoint = max(checkpoints)
    expected = set(range(max_checkpoint + 1))

    if checkpoints != expected:
        raise ValueError(f"Checkpoint harus berurutan dari 0 sampai {max_checkpoint}, ditemukan: {sorted(checkpoints)}.")


def validate_costs(puzzle) -> None:
    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            cost = puzzle.costs[r][c]
            if cost < 0:
                raise ValueError(f"tidak boleh cost negatif di posisi ({r}, {c})")