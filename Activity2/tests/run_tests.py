"""Dependency-free test runner for the Activity 2 tests."""

import importlib.util
from pathlib import Path


test_file = Path(__file__).with_name("test_connect_four_mcts.py")
spec = importlib.util.spec_from_file_location("activity2_tests", test_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

passed = 0
for name in sorted(dir(module)):
    if name.startswith("test_"):
        getattr(module, name)()
        print(f"PASS {name}")
        passed += 1

print(f"{passed} tests passed")
