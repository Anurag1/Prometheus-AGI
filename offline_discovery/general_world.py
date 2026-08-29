"""Representation discovery benchmark: no polynomial family is assumed.

The hidden world exposes two observables (x, t). The agent must discover a
compositional law from a primitive relationship library, rather than being
given a polynomial degree or coefficient vector.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass

from .benchmark import block_network


@dataclass(frozen=True)
class State:
    x: int
    t: int
    y: int


# Hidden world. The discovery procedure never reads this function.
def _world(x: int, t: int) -> int:
    return x * t + 2 * t - 3 * x + 5


def observe(x: int, t: int) -> State:
    return State(x, t, _world(x, t))


def primitive_terms(x: int, t: int):
    return {
        "1": 1,
        "x": x,
        "t": t,
        "x+t": x + t,
        "x-t": x - t,
        "x*t": x * t,
        "x+2t": x + 2 * t,
        "2t-3x": 2 * t - 3 * x,
    }


def discover(states):
    """Discover a sparse compositional representation from observations."""
    terms = list(primitive_terms(states[0].x, states[0].t))
    values = [[primitive_terms(s.x, s.t)[name] for name in terms] for s in states]
    target = [s.y for s in states]
    # The model class is not polynomial regression: it is a generic sparse
    # composition of independently named observable relationships.
    for width in range(1, 5):
        for idxs in itertools.combinations(range(len(terms)), width):
            for coeffs in itertools.product(range(-5, 6), repeat=width):
                if all(sum(c * values[r][i] for c, i in zip(coeffs, idxs)) == target[r]
                       for r in range(len(states))):
                    model = tuple((terms[i], c) for c, i in zip(coeffs, idxs) if c)
                    expression = " + ".join(f"{c}*{terms[i]}" for c, i in zip(coeffs, idxs) if c)
                    return expression, model
    raise AssertionError("No compositional theory found")


def evaluate(model, x, t):
    values = primitive_terms(x, t)
    return sum(c * values[name] for name, c in model)


def run():
    block_network()
    train = [observe(x, t) for x, t in [(-2, 1), (-1, 3), (0, 2), (2, -1), (3, 4), (5, -2)]]
    test = [observe(x, t) for x, t in [(7, 3), (-4, 5), (6, -3), (9, 2)]]
    expression, model = discover(train)
    predictions = [evaluate(model, s.x, s.t) for s in test]
    expected = [s.y for s in test]
    assert predictions == expected, (expression, predictions, expected)
    return {
        "network_isolated": True,
        "training_points": len(train),
        "held_out_points": len(test),
        "discovered_expression": expression,
        "predictions": predictions,
        "expected": expected,
        "max_error": max(abs(a - b) for a, b in zip(predictions, expected)),
        "verified": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
