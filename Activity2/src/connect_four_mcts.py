
from __future__ import annotations

import math
import random


ROWS = 6
COLS = 7


class Board:
    
    def __init__(self, grid=None, player=1):
        
        self.player = player
        if grid is None:
            grid = []

            for x in range(ROWS):
                row = []
                for y in range(COLS):
                    row.append(0)
                grid.append(row)

        self.grid = grid

    def legal_moves(self):
        
        legalmoves = []
        for column in range(COLS):
            if self.grid[0][column] == 0:
                legalmoves.append(column)
        return legalmoves

    def play(self, column):
        if column not in self.legal_moves():
            raise ValueError("Column is full, move is ineligable")

        new_grid = []
        for row in self.grid:
            copied_row = []

            for cell in row:
                copied_row.append(cell)
            new_grid.append(copied_row)


        for row in range(ROWS -1, -1, -1):
            if new_grid[row][column] == 0:
                new_grid[row][column] = self.player
                break

        return Board(new_grid, 3 - self.player)

    def winner(self):

        for row in range(ROWS):
            for column in range(COLS - 3):
                if (
                    self.grid[row][column] 
                == self.grid[row][column+1] 
                == self.grid[row][column+2] 
                ==self.grid[row][column+3]
                != 0
                ):
                    return self.grid[row][column]

        for row in range(ROWS-3):
            for column in range(COLS):
                if (
                    self.grid[row][column] ==
                    self.grid[row+1][column] ==
                    self.grid[row+2][column] ==
                    self.grid[row+3][column]
                    != 0
                    
                ):
                    return self.grid[row][column]

        for row in range(ROWS-3):
            for column in range(COLS-3):
                if (
                    self.grid[row][column] ==
                    self.grid[row+1][column+1] ==
                    self.grid[row+2][column+2] ==
                    self.grid[row+3][column+3]
                    !=0
                ):
                    return self.grid[row][column]

        for row in range(ROWS-3):
            for column in range(3, COLS):
                if (
                    self.grid[row][column] ==
                    self.grid[row+1][column-1] ==
                    self.grid[row+2][column-2] ==
                    self.grid[row+3][column-3]
                    != 0
                ):
                    return self.grid[row][column]
        return 0
        
    def terminal(self):
        return self.winner()!=0 or not self.legal_moves()

class Node:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0.0

    def untried_moves (self):
        used_moves = []

        for child in self.children:
            used_moves.append(child.move)

        moves = []

        for move in self.board.legal_moves():
            if move not in used_moves:
                moves.append(move)

        return moves


def select_child(node):
    best_child = None
    best_score = float("-inf")

    for child in node.children:
        if child.visits == 0:
            return child

        average_value = child.value / child.visits
        exploration = math.sqrt(
            2 * math.log(node.visits) / child.visits
        )
        score = average_value + exploration

        if score > best_score:
            best_score = score
            best_child = child
    return best_child

def rollout(board):
    current_board = board

    while not current_board.terminal():
        moves = current_board.legal_moves()
        move = random.choice(moves)
        current_board = current_board.play(move)

    return current_board.winner()

def choose_move(board, simulations=100, seed=None):
    if seed is not None:
        random.seed(seed)

    root = Node(board)
    original_player = board.player

    for simulation in range(simulations):
        node = root

        #selection
        while(
            not node.untried_moves()
            and node.children
            and not node.board.terminal()
        ):
            node = select_child(node)

        #xpansion
        if node.untried_moves() and not node.board.terminal():
            move = random.choice(node.untried_moves())
            new_board = node.board.play(move)
            child = Node(new_board, node, move)
            node.children.append(child)
            node = child

        #sim
        result = rollout(node.board)

        #backpropagation
        while node is not None:
            node.visits += 1

            if result == original_player:
                node.value += 1

            elif result == 0:
                node.value += 0.5

            node = node.parent

    if not root.children:
        raise ValueError("No move is available")

    best_child = root.children[0]

    for child in root.children:
        if child.visits > best_child.visits:
            best_child = child
    return best_child.move

if __name__ == "__main__":
    simulation_counts = [10, 50, 100, 500]
    seeds = [1, 2, 3, 4, 5]

    print("simulations,seed,selected_move")

    for simulations in simulation_counts:
        for seed in seeds:
            board = Board()
            move = choose_move(
                board,
                simulations=simulations,
                seed=seed
            )

            print(
                simulations,
                seed,
                move,
                sep=","
            )