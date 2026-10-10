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
