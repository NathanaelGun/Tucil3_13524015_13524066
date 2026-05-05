from dataclasses import dataclass
from board import (
    State,
    BoardInfo,
    is_inside,
    is_wall,
    is_lava,
    get_tile,
    get_cost,
)

DIRECTIONS = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

@dataclass
class SlideResult:
    valid: bool
    state: State | None
    move_cost: int
    direction: str
    reason: str = ""
    passed_tiles: list[tuple[int, int]] | None = None

def slide(board_info: BoardInfo, state: State, direction: str) -> SlideResult:
    if direction not in DIRECTIONS:
        return SlideResult(valid=False,
                           state=None,
                           move_cost=0,
                           direction=direction,
                           reason=f"Arah gerakan tidak valid: {direction}",
                           passed_tiles=[],)

    dr, dc = DIRECTIONS[direction]
    current_row = state.row
    current_col = state.col
    next_checkpoint = state.next_checkpoint
    total_cost = 0
    passed_tiles = []
    while True:
        next_row = current_row + dr
        next_col = current_col + dc
        if not is_inside(board_info, next_row, next_col):
            return SlideResult(valid=False,
                               state=None,
                               move_cost=0,
                               direction=direction,
                               reason="Pemain keluar papan.",
                               passed_tiles=passed_tiles,)

        # Tile berikutnya adalah X, berhenti di tile saat ini
        if is_wall(board_info, next_row, next_col):
            if len(passed_tiles) == 0:
                return SlideResult(valid=False,
                                   state=None,move_cost=0,
                                   direction=direction,
                                   reason="Pemain langsung menabrak dinding dan tidak bergerak.",
                                   passed_tiles=passed_tiles,)
            new_state = State(row=current_row,
                              col=current_col,
                              next_checkpoint=next_checkpoint,)
            return SlideResult(valid=True,
                               state=new_state,
                               move_cost=total_cost,
                               direction=direction,
                               reason="",
                               passed_tiles=passed_tiles,)
        # Tile berikutnya dilewati.
        tile = get_tile(board_info, next_row, next_col)

        # Jika melewati lava, game over.
        if is_lava(board_info, next_row, next_col):
            return SlideResult(valid=False,
                               state=None,
                               move_cost=0,
                               direction=direction,
                               reason="Pemain melewati lava.",
                               passed_tiles=passed_tiles + [(next_row, next_col)],)
        # Menjumlahkan cost tile yang dilewati.
        total_cost += get_cost(board_info, next_row, next_col)
        passed_tiles.append((next_row, next_col))

        # Tile angka, cek urutan checkpoint.
        if tile.isdigit():
            checkpoint_number = int(tile)
            if checkpoint_number == next_checkpoint:
                next_checkpoint += 1
            elif checkpoint_number < next_checkpoint:
                pass
            else:
                return SlideResult(valid=False,
                                   state=None,
                                   move_cost=0,
                                   direction=direction,reason=(f"Checkpoint {checkpoint_number} dilewati sebelum checkpoint {next_checkpoint}."),
                                   passed_tiles=passed_tiles,)
        # Update posisi pemain.
        current_row = next_row
        current_col = next_col

def get_valid_neighbors(board_info: BoardInfo, state: State) -> list[SlideResult]:
    """
    Menghasilkan semua gerakan valid dari sebuah state.
    Dipakai untuk UCS, GBFS, dan A*.
    """
    neighbors = []
    for direction in DIRECTIONS:
        result = slide(board_info, state, direction)
        if result.valid:
            neighbors.append(result)
    return neighbors