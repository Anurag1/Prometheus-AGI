import unittest

from offline_discovery.autonomous_lab import run


class AutonomousOfflineDiscoveryTest(unittest.TestCase):
    def test_discovers_verified_theory_without_network(self):
        result = run()
        self.assertTrue(result["network_isolated"])
        theory = result["discovered_theory"]
        self.assertEqual(theory["degree"], 2)
        self.assertEqual(theory["coefficients"], (7.0, -3.0, 2.0))
        self.assertEqual(theory["predictions"], [16.0, 27.0, 42.0, 61.0])
        self.assertEqual(theory["max_error"], 0.0)
        self.assertEqual(result["knowledge_status"], "verified_local_theory")


if __name__ == "__main__":
    unittest.main()
