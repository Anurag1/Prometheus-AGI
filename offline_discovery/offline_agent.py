"""Prometheus-style offline discovery loop.

This mirrors the repository's agent lifecycle without web/market tools:
observe -> compare -> hypothesize -> verify -> persist a discovery record.
The verifier is deliberately independent of the hidden rule.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .benchmark import Observation, discover, evaluate, block_network


class OfflineDiscoveryAgent:
    def __init__(self, workspace: str = "workspace", project_name: str = "offline-discovery"):
        self.project_dir = Path(workspace) / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.project_dir / "knowledge_graph.json"

    def load_memory(self) -> dict:
        if not self.memory_file.exists():
            return {"latest_state": {}, "hypotheses": {}, "discoveries": []}
        return json.loads(self.memory_file.read_text())

    def save_memory(self, record: dict) -> None:
        memory = self.load_memory()
        memory["latest_state"] = record["state"]
        memory["hypotheses"][record["hypothesis_id"]] = record["hypothesis"]
        memory["discoveries"].append(record)
        self.memory_file.write_text(json.dumps(memory, indent=2))

    def run(self, train: Iterable[Observation], held_out: Iterable[Observation]) -> dict:
        block_network()
        train = tuple(train)
        held_out = tuple(held_out)
        hypothesis, degree = discover(train)
        predictions = [evaluate(hypothesis, row.x) for row in held_out]
        expected = [row.y for row in held_out]
        verified = predictions == expected
        record = {
            "mode": "offline",
            "network_isolated": True,
            "state": {str(row.x): row.y for row in train},
            "hypothesis_id": f"poly-degree-{degree}",
            "hypothesis": {"coefficients": hypothesis, "degree": degree},
            "verification": {
                "predictions": predictions,
                "expected": expected,
                "generalizes": verified,
            },
        }
        if not verified:
            raise AssertionError(record)
        self.save_memory(record)
        return record


def run_integration() -> dict:
    agent = OfflineDiscoveryAgent(workspace="/tmp/prometheus-offline")
    train = [Observation(x, 3*x*x + 2*x - 5) for x in (-2, -1, 0, 1, 2)]
    held_out = [Observation(x, 3*x*x + 2*x - 5) for x in (3, 4, 5)]
    return agent.run(train, held_out)


if __name__ == "__main__":
    print(json.dumps(run_integration(), indent=2))
