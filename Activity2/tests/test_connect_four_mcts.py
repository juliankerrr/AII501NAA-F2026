import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from connect_four_mcts import Board, choose_move


def test_empty_board_has_seven_legal_moves():
    assert Board().legal_moves() == list(range(7))


def test_play_places_piece_and_changes_player():
    board = Board().play(3)
    assert board.grid[5][3] == 1
    assert board.player == 2


def test_mcts_returns_legal_reproducible_move():
    board = Board()
    first = choose_move(board, simulations=20, seed=1)
    second = choose_move(board, simulations=20, seed=1)
    assert first in board.legal_moves()
    assert first == second


def test_horizontal_winner():
    grid = [[0] * 7 for _ in range(6)]
    grid[5][0:4] = [1, 1, 1, 1]
    assert Board(grid).winner() == 1


def test_vertical_winner():
    grid = [[0] * 7 for _ in range(6)]
    for row in range(2, 6):
        grid[row][3] = 2
    assert Board(grid).winner() == 2


def test_diagonal_winner():
    grid = [[0] * 7 for _ in range(6)]
    for offset in range(4):
        grid[offset][offset] = 1
    assert Board(grid).winner() == 1


def test_invalid_move_is_rejected():
    grid = [[0] * 7 for _ in range(6)]
    for row in range(6):
        grid[row][0] = 1
    try:
        Board(grid).play(0)
        assert False
    except ValueError:
        assert True
