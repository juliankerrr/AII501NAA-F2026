# AII501NAA Activity 2

This folder contains the source code, tests, experiment data, documentation, and supporting files for Activity 2.

## Project areas

- `src/` — implementation code
- `tests/` — automated tests and test cases
- `data/` — experiment configurations and collected results
- `docs/` — report and logic-problem solutions

## Setup

This basic implementation uses Python 3.10 or newer and has no third-party dependencies.

## Run

From the `Activity2` directory, run:

```bash
PYTHONPATH=src python3 src/connect_four_mcts.py
```

## Test

From the `Activity2` directory, run:

```bash
python3 -m pytest tests
```

If `pytest` is not installed, run the module directly first; the source file includes a basic smoke test through its main entry point.

## Assumptions

The implementation uses a 6-by-7 board, alternating players represented by `1` and `2`, random playouts, and a configurable simulation count. A seed can be supplied for reproducible experiments.

## Assignment coverage

- Connect Four Monte Carlo Tree Search move generator
- Utility-function and parameter experiments
- Propositional-logic validity and satisfiability
- Model counting
- CNF conversion and resolution proof
