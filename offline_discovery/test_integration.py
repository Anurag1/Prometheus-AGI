import json
import unittest

from offline_discovery.benchmark import Observation
from offline_discovery.offline_agent import OfflineDiscoveryAgent


class OfflineAgentIntegrationTest(unittest.TestCase):
    def test_agent_discovers_and_persists_verified_knowledge(self):
        agent = OfflineDiscoveryAgent(workspace="/tmp/prometheus-offline-test", project_name="case")
        train = [Observation(x, 3*x*x + 2*x - 5) for x in (-2, -1, 0, 1, 2)]
        held_out = [Observation(x, 3*x*x + 2*x - 5) for x in (3, 4, 5)]
        result = agent.run(train, held_out)
        self.assertTrue(result["network_isolated"])
        self.assertEqual(result["hypothesis"]["coefficients"], (-5, 2, 3))
        self.assertTrue(result["verification"]["generalizes"])
        memory = agent.load_memory()
        self.assertEqual(len(memory["discoveries"]), 1)
        self.assertEqual(memory["discoveries"][0]["verification"]["predictions"], [28, 51, 80])


if __name__ == "__main__":
    unittest.main()
