from dataclasses import dataclass

@dataclass(frozen=True)
class State:
    # representasi posisi aktor
    row: int
    col: int
    next_checkpoint: int

@dataclass
class BoardInfo:
    rows: int
    cols: int
    board: list[list[str]]
    costs: list[list[int]]
    start: tuple[int, int]
    goal: tuple[int, int]
    checkpoints: dict[int, tuple[int, int]]

def create_board_info(puzzle) -> BoardInfo:
    start = find_start(puzzle)
    goal = find_goal(puzzle)
    checkpoints = find_checkpoint(puzzle)

    return BoardInfo(rows=puzzle.rows,
                     cols=puzzle.cols,
                     board=puzzle.board,
                     costs=puzzle.costs,
                     start=start,
                     goal=goal,
                     checkpoints=checkpoints
    )

def find_start(puzzle) -> tuple[int, int]:
    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            if puzzle.board[r][c] == "Z":
                return (r,c)
    
    raise ValueError("Tidak ditemukan Z")

def find_goal(puzzle) -> tuple[int, int]:
    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            if puzzle.board[r][c] == "O":
                return (r,c)
            
    raise ValueError("Tidak ditemukan goal")

def find_checkpoint(puzzle) -> dict[int, tuple[int, int]]:
    checkpoints = {}
    for r in range(puzzle.rows):
        for c in range(puzzle.cols):
            tile = puzzle.board[r][c]
            if tile.isdigit():
                checkpoints[int(tile)] = (r, c)

    return checkpoints

def create_state_awal(board_info: BoardInfo) -> State:
    start_row, start_col = board_info.start
    return State(row=start_row,
                 col=start_col,
                 next_checkpoint=0)

def is_inside(board_info: BoardInfo, row: int, col: int) -> bool:
    return 0 <= row < board_info.rows and 0 <= col < board_info.cols

def is_wall(board_info: BoardInfo, row: int, col: int) -> bool:
    return board_info.board[row][col] == "X"

def is_lava(board_info: BoardInfo, row: int, col: int) -> bool:
    return board_info.board[row][col] =="L"

def get_tile(board_info: BoardInfo, row: int, col: int) -> str:
    return board_info.board[row][col]

def get_cost(board_info: BoardInfo, row: int, col: int) -> int:
    return board_info.costs[row][col]

def get_total_checkpoints(board_info: BoardInfo) -> int:
    return len(board_info.checkpoints)

def is_all_checkpoints_p(board_info: BoardInfo, state: State) -> bool:
    return state.next_checkpoint >= get_total_checkpoints(board_info)

def is_goal(board_info: BoardInfo, state: State) -> bool:
    posisi_pemain = (state.row, state.col)

    return (posisi_pemain == board_info.goal and is_all_checkpoints_p(board_info, state))

def render_board(board_info: BoardInfo, state: State) -> str:
    rendered_rows = []
    for r in range(board_info.rows):
        row_chars = []
        for c in range(board_info.cols):
            tile = board_info.board[r][c]
            if tile == "Z":
                tile = "*"
            if r == state.row and c == state.col:
                tile = "Z"
            row_chars.append(tile)
        rendered_rows.append("".join(row_chars))
    return "\n".join(rendered_rows)

def print_board(board_info: BoardInfo, state: State) -> None:
    print(render_board(board_info, state))