"""Autonomous closed-world discovery lab.

The agent is not given the governing equation. It receives observations from a
local simulator, proposes competing hypotheses, runs experiments, rejects
wrong hypotheses, and persists the surviving theory. No network is required.
"""
from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .benchmark import block_network


@dataclass(frozen=True)
class Observation:
    x: int
    y: int


# Hidden simulator law. The discovery agent never reads this symbol.
_HIDDEN = lambda x: 2 * x * x - 3 * x + 7


def simulator(x: int) -> int:
    return _HIDDEN(x)


def polynomial_features(x: int):
    return (1, x, x * x, x * x * x)


def solve_linear(rows, values):
    # Small Gaussian elimination, implemented locally to avoid external tools.
    a = [list(map(float, row)) + [float(v)] for row, v in zip(rows, values)]
    m, n = len(a), len(a[0]) - 1
    r = 0
    pivots = []
    for c in range(n):
        pivot = max(range(r, m), key=lambda i: abs(a[i][c]))
        if abs(a[pivot][c]) < 1e-12:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for i in range(m):
            if i != r and abs(a[i][c]) > 1e-12:
                f = a[i][c]
                a[i] = [a[i][j] - f * a[r][j] for j in range(n + 1)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    if len(pivots) < 3:
        raise AssertionError("Insufficient information")
    solution = [0.0] * n
    for i, c in enumerate(pivots):
        solution[c] = a[i][-1]
    return tuple(round(v, 8) for v in solution)


def propose(train):
    # Competing structural hypotheses: constant, linear, quadratic, cubic.
    candidates = []
    for degree in range(4):
        rows = [polynomial_features(o.x)[: degree + 1] for o in train]
        try:
            coeffs = solve_linear(rows, [o.y for o in train])
            candidates.append((degree, coeffs))
        except AssertionError:
            pass
    return candidates


def predict(coeffs, x):
    return sum(c * f for c, f in zip(coeffs, polynomial_features(x)))


def run() -> dict:
    block_network()
    train = [Observation(x, simulator(x)) for x in (-2, -1, 0, 1, 2)]
    experiments = [3, 4, 5, 6]

    hypotheses = propose(train)
    scored = []
    # Active experiment: unseen simulator observations are used only for
    # verification, not hypothesis construction.
    held_out = [Observation(x, simulator(x)) for x in experiments]
    for degree, coeffs in hypotheses:
        predictions = [predict(coeffs, o.x) for o in held_out]
        errors = [abs(p - o.y) for p, o in zip(predictions, held_out)]
        scored.append({"degree": degree, "coefficients": coeffs,
                       "predictions": predictions, "max_error": max(errors)})

    valid = [s for s in scored if s["max_error"] < 1e-8]
    if not valid:
        raise AssertionError({"hypotheses": scored})
    winner = min(valid, key=lambda s: s["degree"])

    record = {
        "network_isolated": True,
        "training": [o.__dict__ for o in train],
        "experiments": [o.__dict__ for o in held_out],
        "competing_hypotheses": scored,
        "discovered_theory": winner,
        "knowledge_status": "verified_local_theory",
    }
    return record


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
