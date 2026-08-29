"""Network-isolated discovery benchmark.

The hidden system is y = 3*x*x + 2*x - 5. The discovery engine receives
only a local training subset, searches a bounded polynomial hypothesis
space, and must predict held-out points exactly.
"""

from __future__ import annotations

import builtins
import importlib
import math
import socket
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class Observation:
    x: int
    y: int


HIDDEN_RULE: Callable[[int], int] = lambda x: 3 * x * x + 2 * x - 5


def block_network() -> None:
    """Fail closed if code attempts common network access during the benchmark."""
    def blocked(*_args, **_kwargs):
        raise RuntimeError("NETWORK_ACCESS_BLOCKED")

    socket.socket = blocked  # type: ignore[assignment]
    socket.create_connection = blocked  # type: ignore[assignment]
    builtins.__import__ = _guard_import(builtins.__import__)


def _guard_import(original_import):
    blocked_modules = {"requests", "urllib", "urllib3", "http", "httpx", "aiohttp"}

    def guarded(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".", 1)[0]
        if root in blocked_modules:
            raise RuntimeError("NETWORK_LIBRARY_BLOCKED")
        return original_import(name, globals, locals, fromlist, level)

    return guarded


def candidate_polynomials(max_degree: int = 3, coefficient_bound: int = 6):
    """Generate small integer-coefficient polynomials deterministically."""
    from itertools import product

    for degree in range(0, max_degree + 1):
        for coefficients in product(range(-coefficient_bound, coefficient_bound + 1), repeat=degree + 1):
            yield coefficients


def evaluate(coefficients: tuple[int, ...], x: int) -> int:
    total = 0
    for coefficient in reversed(coefficients):
        total = total * x + coefficient
    return total


def discover(train: Iterable[Observation]) -> tuple[tuple[int, ...], int]:
    """Find the simplest exact polynomial consistent with all observations."""
    observations = tuple(train)
    best = None
    for coeffs in candidate_polynomials():
        if all(evaluate(coeffs, row.x) == row.y for row in observations):
            complexity = (len(coeffs) - 1, sum(abs(c) for c in coeffs))
            if best is None or complexity < best[0]:
                best = (complexity, coeffs)
    if best is None:
        raise AssertionError("No hypothesis found")
    return best[1], best[0][0]


def run() -> dict:
    block_network()

    local_data = [Observation(x, HIDDEN_RULE(x)) for x in (-2, -1, 0, 1, 2)]
    held_out = [Observation(x, HIDDEN_RULE(x)) for x in (3, 4, 5)]

    hypothesis, degree = discover(local_data)
    predictions = [evaluate(hypothesis, row.x) for row in held_out]
    expected = [row.y for row in held_out]
    passed = predictions == expected

    result = {
        "network_isolated": True,
        "training_points": len(local_data),
        "held_out_points": len(held_out),
        "discovered_coefficients": hypothesis,
        "discovered_degree": degree,
        "held_out_predictions": predictions,
        "held_out_expected": expected,
        "generalizes_to_unseen_data": passed,
    }
    if not passed:
        raise AssertionError(result)
    return result


if __name__ == "__main__":
    result = run()
    print("OFFLINE_DISCOVERY_PASS")
    for key, value in result.items():
        print(f"{key}={value}")
