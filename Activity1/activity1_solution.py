"""AII501 Activity 1 solutions: spam filtering and three-jug BFS."""
from __future__ import annotations

from collections import deque
from email import policy
from email.parser import BytesParser
from pathlib import Path
import re
import shutil
from typing import Iterable


def classify_and_route(
    eml_path: str | Path,
    email_directory: str | Path,
    spam_directory: str | Path,
    allow_list: Iterable[str],
    restrict_list: Iterable[str],
    bad_word_list: Iterable[str],
) -> str:
    """Classify one .eml file and copy it to the required destination.

    Allow-list membership has priority, followed by restrict-list membership,
    followed by the rule that more than five bad-word occurrences means spam.
    """
    source = Path(eml_path)
    msg = BytesParser(policy=policy.default).parsebytes(source.read_bytes())
    sender = msg.get("From", "")
    match = re.search(r"@([A-Za-z0-9.-]+)", sender)
    domain = match.group(1).lower() if match else ""
    allow = {x.lower().lstrip("@").strip() for x in allow_list}
    restrict = {x.lower().lstrip("@").strip() for x in restrict_list}
    bad = {x.lower() for x in bad_word_list}

    if domain in allow:
        label = "non-spam"
    elif domain in restrict:
        label = "spam"
    else:
        body = msg.get_body(preferencelist=("plain",))
        text = body.get_content() if body else ""
        words = re.findall(r"[A-Za-z0-9']+", text.lower())
        label = "spam" if sum(word in bad for word in words) > 5 else "non-spam"

    destination = Path(spam_directory if label == "spam" else email_directory)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination / source.name)
    return label


CAPACITIES = (12, 8, 3)
State = tuple[int, int, int]


def successors(state: State):
    """Yield (action, next_state) for every legal fill, empty, or pour."""
    for i, capacity in enumerate(CAPACITIES):
        if state[i] < capacity:
            s = list(state); s[i] = capacity
            yield f"fill jug {i + 1}", tuple(s)
        if state[i] > 0:
            s = list(state); s[i] = 0
            yield f"empty jug {i + 1}", tuple(s)
    for i in range(3):
        for j in range(3):
            if i == j: continue
            amount = min(state[i], CAPACITIES[j] - state[j])
            if amount:
                s = list(state); s[i] -= amount; s[j] += amount
                yield f"pour jug {i + 1} to jug {j + 1}", tuple(s)


def is_goal(state: State) -> bool:
    return 1 in state


def breadth_first_search(start: State) -> list[tuple[str, State]] | None:
    frontier = deque([start])
    parent: dict[State, tuple[State | None, str | None]] = {start: (None, None)}
    while frontier:
        state = frontier.popleft()
        if is_goal(state):
            path = []
            while parent[state][0] is not None:
                previous, action = parent[state]
                path.append((action, state))
                state = previous
            return list(reversed(path))
        for action, child in successors(state):
            if child not in parent:
                parent[child] = (state, action)
                frontier.append(child)
    return None


if __name__ == "__main__":
    for start in ((0, 0, 0), (12, 0, 0), (0, 8, 0)):
        path = breadth_first_search(start)
        print(f"start={start}, steps={len(path) if path is not None else 'none'}")
        if path:
            for action, state in path: print(f"  {action}: {state}")
