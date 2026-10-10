"""Basic Connect Four board and Monte Carlo Tree Search player."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field


ROWS = 6
COLS = 7


class Board:
    def __init__(self, grid=None, player=1):
        self.grid = [row[:] for row in grid] if grid else [[0] * COLS for _ in range(ROWS)]
        self.player = player

    def legal_moves(self):
        return [column for column in range(COLS) if self.grid[0][column] == 0]

    def play(self, column):
        if column not in self.legal_moves():
            raise ValueError("Column is full or invalid")
        next_grid = [row[:] for row in self.grid]
        for row in range(ROWS - 1, -1, -1):
            if next_grid[row][column] == 0:
                next_grid[row][column] = self.player
                break
        return Board(next_grid, 3 - self.player)

    def winner(self):
        for row in range(ROWS):
            for col in range(COLS):
                player = self.grid[row][col]
                if not player:
                    continue
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    cells = []
                    for offset in range(4):
                        rr, cc = row + dr * offset, col + dc * offset
                        if 0 <= rr < ROWS and 0 <= cc < COLS:
                            cells.append(self.grid[rr][cc])
                    if cells == [player] * 4:
                        return player
        return 0

    def terminal(self):
        return bool(self.winner()) or not self.legal_moves()


@dataclass
class Node:
    board: Board
    parent: "Node | None" = None
    move: int | None = None
    children: list["Node"] = field(default_factory=list)
    visits: int = 0
    value: float = 0.0

    def untried_moves(self):
        used = {child.move for child in self.children}
        return [move for move in self.board.legal_moves() if move not in used]


def _select_child(node):
    return max(
        node.children,
        key=lambda child: child.value / child.visits
        + math.sqrt(2 * math.log(node.visits) / child.visits),
    )


def _rollout(board, rng):
    current = board
    while not current.terminal():
        current = current.play(rng.choice(current.legal_moves()))
    winner = current.winner()
    return 0.5 if winner == 0 else (1.0 if winner == board.player else 0.0)


def choose_move(board, simulations=100, seed=None):
    """Return a move using a small, reproducible MCTS search."""
    if board.terminal():
        raise ValueError("Cannot choose a move from a terminal board")
    rng = random.Random(seed)
    root = Node(board)

    for _ in range(simulations):
        node = root
        while not node.untried_moves() and node.children and not node.board.terminal():
            node = _select_child(node)
        if node.untried_moves() and not node.board.terminal():
            move = rng.choice(node.untried_moves())
            child = Node(node.board.play(move), node, move)
            node.children.append(child)
            node = child
        result = _rollout(node.board, rng)
        while node:
            node.visits += 1
            node.value += result
            node = node.parent

    return max(root.children, key=lambda child: child.visits).move


if __name__ == "__main__":
    print("Suggested move:", choose_move(Board(), simulations=100, seed=7))
