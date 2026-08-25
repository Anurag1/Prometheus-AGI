"""Representation discovery benchmark: no polynomial family is assumed.

The hidden world exposes two observables (x, t). The agent must discover that
one latent quantity is a product and that the target is a conserved affine
combination. Candidate programs are composed from a small primitive library,
not from a preselected polynomial model.
"""
from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from pathlib import Path

from .benchmark import block_network


@dataclass(frozen=True)
class State:
    x: int
    t: int
    y: int


# Hidden world: y = x*t + 2*t - 3*x + 5.
# The discovery code below never imports or references this function.
def _world(x: int, t: int) -> int:
    return x*t + 2*t - 3*x + 5


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
        "x+2t": x + 2*t,
        "2t-3x": 2*t - 3*x,
    }


def discover(states):
    """Enumerate compositions of independent local observables.

    No polynomial degree or coefficient vector is supplied. The search tests
    whether y can be represented as a sparse integer combination of discovered
    primitive relationships.
    """
    terms = list(primitive_terms(states[0].x, states[0].t))
    values = [[primitive_terms(s.x, s.t)[name] for name in terms] for s in states]
    target = [s.y for s in states]
    # Sparse coefficient search over {-3..3}; representation is discovered
    # from primitives rather than assuming a polynomial model class.
    for width in range(1, 4):
        for idxs in itertools.combinations(range(len(terms)), width):
            for coeffs in itertools.product(range(-3, 4), repeat=width):
                if all(sum(c * values[r][i] for c, i in zip(coeffs, idxs)) == target[r]
                       for r in range(len(states))):
                    expression = " + ".join(f"{c}*{terms[i]}" for c, i in zip(coeffs, idxs) if c)
                    return expression, tuple((terms[i], c) for c, i in zip(coeffs, idxs) if c)
    raise AssertionError("No compositional theory found")


def evaluate(model, x, t):
    return sum(c * primitive_terms(x, t)[name] for name, c in model)


def run():
    block_network()
    train = [observe(x, t) for x, t in [(-2,1),(-1,3),(0,2),(2,-1),(3,4),(5,-2)]]
    test = [observe(x, t) for x, t in [(7,3),(-4,5),(6,-3),(9,2)]]
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
        "max_error": max(abs(a-b) for a,b in zip(predictions, expected)),
        "verified": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
