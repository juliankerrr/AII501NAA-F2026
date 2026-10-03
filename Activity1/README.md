# AII501NAA Activity 1

## Files

- `activity1_solution.py` contains the spam-filter agent and three-jug BFS.
- `test_activity1.py` contains automated tests.
- `test_data/sample_email.eml` is sample email input.

## Run

```bash
python activity1_solution.py
```

## Test

```bash
python -m unittest -v
```

The spam filter checks the allow list first, the restrict list second, and then
counts bad-word occurrences in readable plain text. More than five matches means
spam. The jug solver uses breadth-first search with a visited set and returns a
shortest-action path to a state containing one gallon.
