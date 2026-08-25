import unittest

from offline_discovery.benchmark import evaluate, discover, run, Observation


class OfflineDiscoveryTest(unittest.TestCase):
    def test_discovers_hidden_rule_from_local_observations(self):
        train = [
            Observation(-2, 3 * 4 - 4 - 5),
            Observation(-1, 3 - 2 - 5),
            Observation(0, -5),
            Observation(1, 3 + 2 - 5),
            Observation(2, 12 + 4 - 5),
        ]
        hypothesis, degree = discover(train)
        self.assertEqual(hypothesis, (-5, 2, 3))
        self.assertEqual(degree, 2)
        self.assertEqual([evaluate(hypothesis, x) for x in (3, 4, 5)], [28, 51, 80])

    def test_end_to_end(self):
        result = run()
        self.assertTrue(result["network_isolated"])
        self.assertTrue(result["generalizes_to_unseen_data"])
        self.assertEqual(tuple(result["discovered_coefficients"]), (-5, 2, 3))


if __name__ == "__main__":
    unittest.main()
